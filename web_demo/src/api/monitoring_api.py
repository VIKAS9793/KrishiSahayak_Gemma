"""
API endpoints for monitoring the RAG system.
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, Optional
import logging
from rag.monitoring import get_rag_metrics, reset_rag_metrics

# Configure logging
logger = logging.getLogger(__name__)

# Create API router
router = APIRouter(
    prefix="/monitoring",
    tags=["monitoring"],
    responses={404: {"description": "Not found"}},
)

@router.get(
    "/metrics",
    response_model=Dict[str, Any],
    summary="Get system metrics",
    description="Retrieve current system metrics including search statistics and system health."
)
async def get_metrics() -> Dict[str, Any]:
    """Get current system metrics including search statistics and system health.
    
    Returns:
        Dict containing system metrics and status
    """
    try:
        metrics = get_rag_metrics()
        return {
            "status": "success",
            "data": metrics,
            "timestamp": metrics.get("system", {}).get("timestamp")
        }
    except Exception as e:
        logger.error("Error retrieving metrics: %s", str(e), exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve metrics"
        ) from e

@router.post(
    "/metrics/reset",
    response_model=Dict[str, Any],
    summary="Reset metrics",
    description="Reset all metrics and return the state before reset. Requires authentication in production."
)
async def reset_metrics() -> Dict[str, Any]:
    """Reset all metrics and return the state before reset.
    
    Note:
        Requires authentication in production.
        
    Returns:
        Dict containing previous metrics and reset status
    """
    try:
        previous_metrics = reset_rag_metrics()
        return {
            "status": "success",
            "message": "Metrics have been reset",
            "previous_metrics": previous_metrics,
            "timestamp": previous_metrics.get("system", {}).get("timestamp")
        }
    except Exception as e:
        logger.error("Error resetting metrics: %s", str(e), exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to reset metrics"
        ) from e

@router.get(
    "/health",
    response_model=Dict[str, Any],
    summary="Health check",
    description="Basic health check endpoint for the monitoring service."
)
async def health_check() -> Dict[str, Any]:
    """Perform a basic health check of the monitoring service.
    
    Returns:
        Dict containing health status and version information
    """
    try:
        metrics = get_rag_metrics()
        return {
            "status": "healthy",
            "uptime_seconds": metrics.get("uptime", 0),
            "version": "1.0.0",
            "timestamp": metrics.get("system", {}).get("timestamp")
        }
    except Exception as e:
        logger.error("Health check failed: %s", str(e), exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Health check failed"
        ) from e
