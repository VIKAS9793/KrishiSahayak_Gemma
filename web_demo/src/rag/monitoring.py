"""
Monitoring and metrics collection for the RAG system.
"""
import time
import psutil
from datetime import datetime
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class RAGMonitor:
    """A class to monitor and report RAG system metrics."""
    
    def __init__(self):
        """Initialize the RAGMonitor with default metrics."""
        self.metrics = {
            'start_time': time.time(),
            'total_searches': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'total_search_time': 0.0,
            'errors': 0,
            'rate_limited_requests': 0,
            'last_reset': datetime.now().isoformat()
        }
        self.process = psutil.Process()

    def record_search(self, cache_hit: bool, search_time: float) -> None:
        """Record search metrics.
        
        Args:
            cache_hit: Whether the search result was served from cache
            search_time: Time taken for the search in seconds
        """
        self.metrics['total_searches'] += 1
        self.metrics['total_search_time'] += search_time
        
        if cache_hit:
            self.metrics['cache_hits'] += 1
        else:
            self.metrics['cache_misses'] += 1
            
        logger.debug(
            "Search recorded - Cache Hit: %s, Time: %.4fs",
            cache_hit,
            search_time
        )

    def record_error(self, error_type: str = "unknown"):
        """Record error metrics."""
        self.metrics['errors'] += 1
        logger.error(f"Error recorded - Type: {error_type}")

    def record_rate_limit(self):
        """Record rate limit events."""
        self.metrics['rate_limited_requests'] += 1
        logger.warning("Rate limit event recorded")

    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics with system information.
        
        Returns:
            Dict containing system and search metrics
        """
        # Calculate derived metrics
        metrics = self.metrics.copy()
        metrics['uptime'] = time.time() - metrics['start_time']
        
        if metrics['total_searches'] > 0:
            metrics['avg_search_time'] = (
                metrics['total_search_time'] / metrics['total_searches']
            )
            metrics['cache_hit_rate'] = (
                metrics['cache_hits'] / metrics['total_searches']
            )
        else:
            metrics['avg_search_time'] = 0.0
            metrics['cache_hit_rate'] = 0.0
            
        # Add system metrics
        try:
            process = psutil.Process()
            metrics['system'] = {
                'cpu_percent': psutil.cpu_percent(),
                'memory_usage_mb': process.memory_info().rss / (1024 * 1024),
                'process_memory_percent': process.memory_percent(),
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error("Failed to get system metrics: %s", str(e))
            metrics['system'] = {
                'error': 'Failed to collect system metrics',
                'timestamp': datetime.now().isoformat()
            }
        
        return metrics

    def reset_metrics(self):
        """Reset all metrics except uptime."""
        self.metrics.update({
            'total_searches': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'total_search_time': 0.0,
            'errors': 0,
            'rate_limited_requests': 0,
            'last_reset': datetime.now().isoformat()
        })
        logger.info("Metrics have been reset")

# Global monitor instance
monitor = RAGMonitor()

def get_rag_metrics() -> Dict[str, Any]:
    """Get current RAG metrics.
    
    Returns:
        Dict containing current metrics
    """
    return monitor.get_metrics()

def reset_rag_metrics() -> Dict[str, Any]:
    """Reset RAG metrics and return the state before reset.
    
    Returns:
        Dict containing metrics before reset
    """
    metrics = monitor.get_metrics()
    monitor.reset_metrics()
    return metrics
