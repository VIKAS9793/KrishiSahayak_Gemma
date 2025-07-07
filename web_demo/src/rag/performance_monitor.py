# ==============================================================================
# RAG Performance Monitor & Validator
# ==============================================================================

import time
import psutil
import numpy as np
import pandas as pd
from pathlib import Path
import pickle
import faiss
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any, Tuple
import logging
from dataclasses import dataclass
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class PerformanceMetrics:
    """Data class for performance metrics."""
    search_time: float
    memory_usage: float
    cpu_usage: float
    query_length: int
    results_count: int
    relevance_score: float

class RAGPerformanceMonitor:
    """Monitor and validate RAG system performance."""
    
    def __init__(self, index_path: str, texts_path: str, model_name: str = "all-MiniLM-L6-v2"):
        self.index_path = index_path
        self.texts_path = texts_path
        self.model_name = model_name
        self.index = None
        self.texts = []
        self.model = None
        self.metrics_history = []
        
    def load_rag_system(self):
        """Load the complete RAG system."""
        logger.info("Loading RAG system components...")
        
        try:
            # Load FAISS index
            self.index = faiss.read_index(self.index_path)
            logger.info(f"✅ FAISS index loaded: {self.index.ntotal} vectors")
            
            # Load texts
            with open(self.texts_path, 'rb') as f:
                self.texts = pickle.load(f)
            logger.info(f"✅ Text data loaded: {len(self.texts)} chunks")
            
            # Load embedding model
            self.model = SentenceTransformer(self.model_name)
            logger.info(f"✅ Embedding model loaded: {self.model_name}")
            
        except Exception as e:
            logger.error(f"❌ Failed to load RAG system: {e}")
            raise
    
    def benchmark_search(self, query: str, top_k: int = 5) -> Tuple[List[str], PerformanceMetrics]:
        """Benchmark a single search query."""
        if not self.index or not self.model:
            raise ValueError("RAG system not loaded")
        
        # Monitor system resources
        process = psutil.Process()
        start_memory = process.memory_info().rss / 1024 / 1024  # MB
        start_cpu = process.cpu_percent()
        
        # Perform search
        start_time = time.time()
        
        # Generate query embedding
        query_embedding = self.model.encode([query], normalize_embeddings=True)
        
        # Search in FAISS index
        similarities, indices = self.index.search(query_embedding.astype(np.float32), top_k)
        
        # Retrieve results
        results = []
        for i, idx in enumerate(indices[0]):
            if idx != -1:  # Valid result
                results.append({
                    'text': self.texts[idx],
                    'score': float(similarities[0][i]),
                    'index': int(idx)
                })
        
        end_time = time.time()
        
        # Calculate metrics
        end_memory = process.memory_info().rss / 1024 / 1024  # MB
        end_cpu = process.cpu_percent()
        
        metrics = PerformanceMetrics(
            search_time=end_time - start_time,
            memory_usage=end_memory - start_memory,
            cpu_usage=end_cpu - start_cpu,
            query_length=len(query),
            results_count=len(results),
            relevance_score=np.mean([r['score'] for r in results]) if results else 0.0
        )
        
        self.metrics_history.append(metrics)
        return results, metrics
    
    def run_benchmark_suite(self, test_queries: List[str]) -> Dict[str, Any]:
        """Run comprehensive benchmark suite."""
        logger.info(f"Running benchmark suite with {len(test_queries)} queries...")
        
        all_results = []
        all_metrics = []
        
        for i, query in enumerate(test_queries):
            logger.info(f"Testing query {i+1}/{len(test_queries)}: {query[:50]}...")
            
            try:
                results, metrics = self.benchmark_search(query)
                all_results.append({
                    'query': query,
                    'results': results,
                    'metrics': metrics
                })
                all_metrics.append(metrics)
                
            except Exception as e:
                logger.error(f"❌ Query {i+1} failed: {e}")
        
        # Calculate summary statistics
        summary = self._calculate_summary_stats(all_metrics)
        
        return {
            'individual_results': all_results,
            'summary_stats': summary,
            'total_queries': len(test_queries),
            'successful_queries': len(all_metrics)
        }
    
    def _calculate_summary_stats(self, metrics: List[PerformanceMetrics]) -> Dict[str, float]:
        """Calculate summary statistics from metrics."""
        if not metrics:
            return {}
        
        search_times = [m.search_time for m in metrics]
        memory_usage = [m.memory_usage for m in metrics]
        cpu_usage = [m.cpu_usage for m in metrics]
        relevance_scores = [m.relevance_score for m in metrics]
        
        return {
            'avg_search_time': np.mean(search_times),
            'max_search_time': np.max(search_times),
            'min_search_time': np.min(search_times),
            'p95_search_time': np.percentile(search_times, 95),
            'avg_memory_usage': np.mean(memory_usage),
            'avg_cpu_usage': np.mean(cpu_usage),
            'avg_relevance_score': np.mean(relevance_scores),
            'min_relevance_score': np.min(relevance_scores),
            'max_relevance_score': np.max(relevance_scores)
        }
    
    def validate_index_integrity(self) -> Dict[str, Any]:
        """Validate the integrity of the RAG index."""
        logger.info("Validating index integrity...")
        
        validation_results = {
            'index_size': self.index.ntotal if self.index else 0,
            'texts_count': len(self.texts),
            'dimension': self.index.d if self.index else 0,
            'is_trained': self.index.is_trained if self.index else False,
            'issues': []
        }
        
        # Check size consistency
        if self.index and len(self.texts) != self.index.ntotal:
            validation_results['issues'].append(
                f"Size mismatch: {len(self.texts)} texts vs {self.index.ntotal} vectors"
            )
        
        # Check for empty texts
        empty_texts = sum(1 for text in self.texts if not text.strip())
        if empty_texts > 0:
            validation_results['issues'].append(f"Found {empty_texts} empty text chunks")
        
        # Test random searches
        try:
            test_embedding = np.random.random((1, self.index.d)).astype(np.float32)
            _, indices = self.index.search(test_embedding, 5)
            if np.any(indices[0] == -1):
                validation_results['issues'].append("Index search returning invalid indices")
        except Exception as e:
            validation_results['issues'].append(f"Index search test failed: {e}")
        
        validation_results['is_valid'] = len(validation_results['issues']) == 0
        
        return validation_results
    
    def generate_performance_report(self, output_path: str = "performance_report.json"):
        """Generate comprehensive performance report."""
        logger.info("Generating performance report...")
        
        # Sample test queries for agricultural domain
        test_queries = [
            "What are the best practices for crop rotation?",
            "How to manage pest control in organic farming?",
            "What fertilizers are recommended for wheat cultivation?",
            "How to improve soil health naturally?",
            "What are the signs of nutrient deficiency in plants?",
            "Best irrigation techniques for water conservation",
            "How to prevent crop diseases during monsoon?",
            "Organic farming methods for sustainable agriculture",
            "What are the benefits of companion planting?",
            "How to increase crop yield without chemicals?"
        ]
        
        # Load RAG system
        self.load_rag_system()
        
        # Validate index
        validation_results = self.validate_index_integrity()
        
        # Run benchmarks
        benchmark_results = self.run_benchmark_suite(test_queries)
        
        # System information
        system_info = {
            'cpu_count': psutil.cpu_count(),
            'memory_total': psutil.virtual_memory().total / 1024 / 1024 / 1024,  # GB
            'python_version': f"{psutil.sys.version_info.major}.{psutil.sys.version_info.minor}",
            'model_name': self.model_name
        }
        
        # Compile report
        report = {
            'timestamp': pd.Timestamp.now().isoformat(),
            'system_info': system_info,
            'index_validation': validation_results,
            'benchmark_results': benchmark_results,
            'recommendations': self._generate_recommendations(benchmark_results, validation_results)
        }
        
        # Save report
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        logger.info(f"✅ Performance report saved to: {output_path}")
        
        # Print summary
        self._print_performance_summary(benchmark_results, validation_results)
        
        return report
    
    def _generate_recommendations(self, benchmark_results: Dict, validation_results: Dict) -> List[str]:
        """Generate performance recommendations."""
        recommendations = []
        
        if benchmark_results['summary_stats']:
            stats = benchmark_results['summary_stats']
            
            # Search time recommendations
            if stats['avg_search_time'] > 0.1:
                recommendations.append(
                    "Consider using GPU acceleration or a smaller embedding model for faster search"
                )
            
            if stats['p95_search_time'] > 0.5:
                recommendations.append(
                    "95th percentile search time is high. Consider index optimization or caching"
                )
            
            # Relevance score recommendations
            if stats['avg_relevance_score'] < 0.5:
                recommendations.append(
                    "Low relevance scores detected. Consider improving text chunking or using a better embedding model"
                )
            
            # Memory usage recommendations
            if stats['avg_memory_usage'] > 100:
                recommendations.append(
                    "High memory usage detected. Consider batch processing or streaming for large datasets"
                )
        
        # Validation issues
        if validation_results['issues']:
            recommendations.extend([
                f"Fix validation issue: {issue}" for issue in validation_results['issues']
            ])
        
        # Index size recommendations
        if validation_results['index_size'] < 100:
            recommendations.append(
                "Small index size. Consider adding more diverse training data for better coverage"
            )
        
        return recommendations
    
    def _print_performance_summary(self, benchmark_results: Dict, validation_results: Dict):
        """Print performance summary to console."""
        print("\n" + "="*80)
        print("📊 RAG SYSTEM PERFORMANCE REPORT")
        print("="*80)
        
        # Index validation
        print(f"🔍 Index Validation: {'✅ PASSED' if validation_results['is_valid'] else '❌ FAILED'}")
        print(f"📄 Total Documents: {validation_results['texts_count']}")
        print(f"🔢 Vector Dimension: {validation_results['dimension']}")
        print(f"🎯 Index Size: {validation_results['index_size']} vectors")
        
        if validation_results['issues']:
            print(f"⚠️  Issues Found: {len(validation_results['issues'])}")
            for issue in validation_results['issues']:
                print(f"   - {issue}")
        
        # Benchmark results
        if benchmark_results['summary_stats']:
            stats = benchmark_results['summary_stats']
            print(f"\n⚡ Search Performance:")
            print(f"   • Average Search Time: {stats['avg_search_time']:.4f}s")
            print(f"   • 95th Percentile: {stats['p95_search_time']:.4f}s")
            print(f"   • Min/Max: {stats['min_search_time']:.4f}s / {stats['max_search_time']:.4f}s")
            
            print(f"\n🎯 Relevance Scores:")
            print(f"   • Average: {stats['avg_relevance_score']:.4f}")
            print(f"   • Min/Max: {stats['min_relevance_score']:.4f} / {stats['max_relevance_score']:.4f}")
            
            print(f"\n💾 Resource Usage:")
            print(f"   • Average Memory: {stats['avg_memory_usage']:.2f} MB")
            print(f"   • Average CPU: {stats['avg_cpu_usage']:.2f}%")
        
        print(f"\n📈 Test Results: {benchmark_results['successful_queries']}/{benchmark_results['total_queries']} queries successful")
        print("="*80)

# ==============================================================================
# Usage Example
# ==============================================================================

def main():
    """Main function to run performance monitoring."""
    
    # Paths to archived demo dataset
    index_path = "../../data/_archive/knowledge_base_v0_generic_46-class.faiss"
    texts_path = "../../data/_archive/knowledge_base_v0_generic_46-class_text.pkl"
    
    # Create monitor
    monitor = RAGPerformanceMonitor(index_path, texts_path)
    
    # Generate performance report
    report = monitor.generate_performance_report("rag_performance_report.json")
    
    print("\n✅ Performance monitoring complete!")
    print("📊 Report saved to: rag_performance_report.json")

if __name__ == "__main__":
    main()
