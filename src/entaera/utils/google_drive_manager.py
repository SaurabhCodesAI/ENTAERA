"""
ENTAERA Google Drive Integration
4TB storage for models, cache, and demo outputs
"""

import os
import json
import pickle
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)

class GoogleDriveManager:
    """Manages 4TB Google Drive storage for ENTAERA."""
    
    def __init__(self, cache_dir: str = "ENTAERA_Cache"):
        """Initialize Google Drive manager."""
        self.cache_dir = cache_dir
        self.local_cache = Path("./cache")
        self.local_cache.mkdir(exist_ok=True)
        
        # Track what's stored where
        self.drive_index_file = self.local_cache / "drive_index.json"
        self.drive_index = self._load_drive_index()
        
        # Storage quotas (4TB = 4000GB)
        self.max_storage_gb = 4000
        self.current_usage_gb = 0
        
        logger.info(f"Initialized GoogleDriveManager with {cache_dir}")
    
    def _load_drive_index(self) -> Dict[str, Any]:
        """Load the index of what's stored on Drive."""
        if self.drive_index_file.exists():
            try:
                with open(self.drive_index_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Could not load drive index: {e}")
        
        return {
            "embeddings": {},
            "models": {},
            "code_cache": {},
            "demo_outputs": {},
            "analysis_results": {},
            "total_size_gb": 0
        }
    
    def _save_drive_index(self):
        """Save the drive index."""
        try:
            with open(self.drive_index_file, 'w') as f:
                json.dump(self.drive_index, f, indent=2)
        except Exception as e:
            logger.error(f"Could not save drive index: {e}")
    
    def cache_embeddings(self, embeddings: Dict[str, Any], key: str) -> bool:
        """Cache embeddings to Google Drive."""
        try:
            # Save locally first
            local_file = self.local_cache / f"embeddings_{key}.pkl"
            with open(local_file, 'wb') as f:
                pickle.dump(embeddings, f)
            
            # Simulate Drive upload (replace with actual Google Drive API)
            file_size_mb = local_file.stat().st_size / (1024 * 1024)
            
            # Add to index
            self.drive_index["embeddings"][key] = {
                "file_path": f"{self.cache_dir}/embeddings_{key}.pkl",
                "size_mb": file_size_mb,
                "created_at": str(Path(local_file).stat().st_mtime),
                "local_copy": str(local_file)
            }
            
            self.drive_index["total_size_gb"] += file_size_mb / 1024
            self._save_drive_index()
            
            logger.info(f"Cached embeddings {key} to Drive ({file_size_mb:.2f}MB)")
            return True
            
        except Exception as e:
            logger.error(f"Failed to cache embeddings: {e}")
            return False
    
    def cache_generated_code(self, code: str, metadata: Dict[str, Any]) -> bool:
        """Cache generated code to Google Drive."""
        try:
            key = f"code_{metadata.get('language', 'unknown')}_{int(time.time())}"
            
            # Save locally
            local_file = self.local_cache / f"{key}.json"
            code_data = {
                "code": code,
                "metadata": metadata,
                "timestamp": time.time()
            }
            
            with open(local_file, 'w') as f:
                json.dump(code_data, f, indent=2)
            
            # Simulate Drive upload
            file_size_mb = local_file.stat().st_size / (1024 * 1024)
            
            self.drive_index["code_cache"][key] = {
                "file_path": f"{self.cache_dir}/{key}.json",
                "size_mb": file_size_mb,
                "language": metadata.get('language'),
                "type": metadata.get('type'),
                "local_copy": str(local_file)
            }
            
            self.drive_index["total_size_gb"] += file_size_mb / 1024
            self._save_drive_index()
            
            logger.info(f"Cached generated code {key} to Drive")
            return True
            
        except Exception as e:
            logger.error(f"Failed to cache code: {e}")
            return False
    
    def cache_analysis_results(self, analysis: Dict[str, Any], file_path: str) -> bool:
        """Cache code analysis results to Google Drive."""
        try:
            import hashlib
            key = hashlib.md5(file_path.encode()).hexdigest()
            
            # Save locally
            local_file = self.local_cache / f"analysis_{key}.json"
            with open(local_file, 'w') as f:
                json.dump(analysis, f, indent=2)
            
            # Simulate Drive upload
            file_size_mb = local_file.stat().st_size / (1024 * 1024)
            
            self.drive_index["analysis_results"][key] = {
                "file_path": f"{self.cache_dir}/analysis_{key}.json",
                "size_mb": file_size_mb,
                "original_file": file_path,
                "local_copy": str(local_file)
            }
            
            self.drive_index["total_size_gb"] += file_size_mb / 1024
            self._save_drive_index()
            
            logger.info(f"Cached analysis results for {file_path} to Drive")
            return True
            
        except Exception as e:
            logger.error(f"Failed to cache analysis: {e}")
            return False
    
    def sync_demo_outputs(self, demo_dir: Path) -> bool:
        """Sync demo outputs to Google Drive."""
        try:
            if not demo_dir.exists():
                return False
            
            total_size = 0
            synced_files = []
            
            for file_path in demo_dir.rglob("*"):
                if file_path.is_file():
                    relative_path = file_path.relative_to(demo_dir)
                    file_size_mb = file_path.stat().st_size / (1024 * 1024)
                    
                    # Add to index
                    key = str(relative_path).replace(os.sep, "_")
                    self.drive_index["demo_outputs"][key] = {
                        "file_path": f"{self.cache_dir}/demos/{relative_path}",
                        "size_mb": file_size_mb,
                        "local_path": str(file_path)
                    }
                    
                    total_size += file_size_mb
                    synced_files.append(str(relative_path))
            
            self.drive_index["total_size_gb"] += total_size / 1024
            self._save_drive_index()
            
            logger.info(f"Synced {len(synced_files)} demo files to Drive ({total_size:.2f}MB)")
            return True
            
        except Exception as e:
            logger.error(f"Failed to sync demo outputs: {e}")
            return False
    
    def get_storage_stats(self) -> Dict[str, Any]:
        """Get storage usage statistics."""
        return {
            "total_storage_gb": self.max_storage_gb,
            "used_storage_gb": self.drive_index["total_size_gb"],
            "free_storage_gb": self.max_storage_gb - self.drive_index["total_size_gb"],
            "usage_percent": (self.drive_index["total_size_gb"] / self.max_storage_gb) * 100,
            "cached_embeddings": len(self.drive_index["embeddings"]),
            "cached_code": len(self.drive_index["code_cache"]),
            "cached_analysis": len(self.drive_index["analysis_results"]),
            "demo_outputs": len(self.drive_index["demo_outputs"])
        }
    
    def print_storage_report(self):
        """Print storage usage report."""
        stats = self.get_storage_stats()
        
        print("\n💾 GOOGLE DRIVE STORAGE REPORT")
        print("=" * 50)
        print(f"📊 Storage: {stats['used_storage_gb']:.2f}GB / {stats['total_storage_gb']}GB")
        print(f"📈 Usage: {stats['usage_percent']:.1f}%")
        print(f"💚 Free: {stats['free_storage_gb']:.2f}GB")
        print(f"🔢 Cached Embeddings: {stats['cached_embeddings']}")
        print(f"💻 Cached Code: {stats['cached_code']}")
        print(f"📊 Cached Analysis: {stats['cached_analysis']}")
        print(f"🎬 Demo Outputs: {stats['demo_outputs']}")
    
    def cleanup_old_cache(self, days: int = 30) -> int:
        """Clean up cache older than specified days."""
        import time
        
        current_time = time.time()
        cutoff_time = current_time - (days * 24 * 60 * 60)
        cleaned_count = 0
        
        # Clean embeddings
        to_remove = []
        for key, data in self.drive_index["embeddings"].items():
            if float(data["created_at"]) < cutoff_time:
                to_remove.append(key)
        
        for key in to_remove:
            del self.drive_index["embeddings"][key]
            cleaned_count += 1
        
        # Clean code cache (similar logic for other types)
        to_remove = []
        for key, data in self.drive_index["code_cache"].items():
            # Implement cleanup logic based on your needs
            pass
        
        if cleaned_count > 0:
            self._save_drive_index()
            logger.info(f"Cleaned up {cleaned_count} old cache entries")
        
        return cleaned_count


# Integration with existing ENTAERA systems
class DriveIntegratedCacheManager:
    """Cache manager that uses both local and Google Drive storage."""
    
    def __init__(self):
        self.drive_manager = GoogleDriveManager()
        self.local_cache = {}
    
    async def get_cached_embedding(self, text: str) -> Optional[List[float]]:
        """Get cached embedding, checking local first, then Drive."""
        import hashlib
        key = hashlib.md5(text.encode()).hexdigest()
        
        # Check local cache first
        if key in self.local_cache:
            return self.local_cache[key]
        
        # Check Drive index
        if key in self.drive_manager.drive_index["embeddings"]:
            try:
                # Load from local copy if available
                local_copy = self.drive_manager.drive_index["embeddings"][key]["local_copy"]
                if Path(local_copy).exists():
                    with open(local_copy, 'rb') as f:
                        embeddings = pickle.load(f)
                        self.local_cache[key] = embeddings
                        return embeddings
            except Exception as e:
                logger.warning(f"Could not load cached embedding: {e}")
        
        return None
    
    async def cache_embedding(self, text: str, embedding: List[float]):
        """Cache embedding locally and to Drive."""
        import hashlib
        key = hashlib.md5(text.encode()).hexdigest()
        
        # Cache locally
        self.local_cache[key] = embedding
        
        # Cache to Drive
        embeddings_data = {key: embedding}
        self.drive_manager.cache_embeddings(embeddings_data, key)


# Example usage
def demo_google_drive_integration():
    """Demonstrate Google Drive integration."""
    
    print("🚀 Google Drive Integration Demo")
    print("=" * 40)
    
    drive_manager = GoogleDriveManager()
    
    # Demo caching
    print("\n📦 Caching demo data...")
    
    # Cache some embeddings
    demo_embeddings = {"test_embedding": [0.1, 0.2, 0.3] * 100}
    drive_manager.cache_embeddings(demo_embeddings, "demo_test")
    
    # Cache generated code
    demo_code = "def hello_world():\n    print('Hello from ENTAERA!')"
    demo_metadata = {"language": "python", "type": "function", "demo": True}
    drive_manager.cache_generated_code(demo_code, demo_metadata)
    
    # Cache analysis results
    demo_analysis = {"complexity": 1, "lines": 2, "quality_score": 0.9}
    drive_manager.cache_analysis_results(demo_analysis, "demo_file.py")
    
    # Print storage report
    drive_manager.print_storage_report()
    
    print("\n✅ Google Drive integration demo completed!")

if __name__ == "__main__":
    import time
    demo_google_drive_integration()