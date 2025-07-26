import json
import hashlib
import os
from pathlib import Path
from typing import Optional, Dict, Any
import time

class OutlineCache:
    """Smart caching system for outline extraction"""
    
    def __init__(self, cache_dir: str = "cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self._cache_index_file = self.cache_dir / "cache_index.json"
        self._cache_index = self._load_cache_index()
    
    def _load_cache_index(self) -> Dict[str, Dict]:
        """Load cache index for quick lookups"""
        if self._cache_index_file.exists():
            try:
                with open(self._cache_index_file) as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}
    
    def _save_cache_index(self):
        """Save cache index"""
        try:
            with open(self._cache_index_file, 'w') as f:
                json.dump(self._cache_index, f, indent=2)
        except Exception:
            pass  # Fail silently for cache operations
    
    def get_cache_key(self, pdf_path: str) -> str:
        """Generate cache key based on file hash and modification time"""
        try:
            stat = os.stat(pdf_path)
            content = f"{pdf_path}:{stat.st_mtime}:{stat.st_size}"
            return hashlib.md5(content.encode()).hexdigest()
        except Exception:
            return hashlib.md5(pdf_path.encode()).hexdigest()
    
    def get_cached_outline(self, pdf_path: str) -> Optional[Dict[str, Any]]:
        """Retrieve cached outline if valid"""
        cache_key = self.get_cache_key(pdf_path)
        
        # Check index first
        if cache_key not in self._cache_index:
            return None
        
        cache_file = self.cache_dir / f"{cache_key}.json"
        
        if cache_file.exists():
            try:
                # Check if cache is still valid (not older than 30 days)
                cache_age = time.time() - cache_file.stat().st_mtime
                if cache_age > 30 * 24 * 3600:  # 30 days
                    self._remove_cache_entry(cache_key)
                    return None
                
                with open(cache_file) as f:
                    cached_data = json.load(f)
                
                # Validate cache structure
                if self._is_valid_cache(cached_data):
                    return cached_data
                else:
                    self._remove_cache_entry(cache_key)
                    return None
                    
            except Exception:
                self._remove_cache_entry(cache_key)
                return None
        
        return None
    
    def cache_outline(self, pdf_path: str, outline_data: Dict[str, Any]):
        """Cache outline data"""
        try:
            cache_key = self.get_cache_key(pdf_path)
            cache_file = self.cache_dir / f"{cache_key}.json"
            
            # Add metadata
            cache_entry = {
                'pdf_path': pdf_path,
                'cached_at': time.time(),
                'data': outline_data
            }
            
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_entry, f, ensure_ascii=False, indent=2)
            
            # Update index
            self._cache_index[cache_key] = {
                'pdf_path': pdf_path,
                'cached_at': time.time()
            }
            self._save_cache_index()
            
        except Exception:
            pass  # Fail silently for cache operations
    
    def _is_valid_cache(self, cached_data: Dict) -> bool:
        """Validate cache data structure"""
        required_keys = ['data']
        if not all(key in cached_data for key in required_keys):
            return False
        
        data = cached_data['data']
        return isinstance(data, dict) and 'title' in data and 'outline' in data
    
    def _remove_cache_entry(self, cache_key: str):
        """Remove cache entry"""
        try:
            cache_file = self.cache_dir / f"{cache_key}.json"
            if cache_file.exists():
                cache_file.unlink()
            
            if cache_key in self._cache_index:
                del self._cache_index[cache_key]
                self._save_cache_index()
        except Exception:
            pass
    
    def clear_cache(self):
        """Clear all cache"""
        try:
            for cache_file in self.cache_dir.glob("*.json"):
                cache_file.unlink()
            self._cache_index = {}
            self._save_cache_index()
        except Exception:
            pass
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        try:
            cache_files = list(self.cache_dir.glob("*.json"))
            total_size = sum(f.stat().st_size for f in cache_files if f.name != "cache_index.json")
            
            return {
                'total_entries': len(self._cache_index),
                'total_size_mb': total_size / (1024 * 1024),
                'cache_dir': str(self.cache_dir)
            }
        except Exception:
            return {'total_entries': 0, 'total_size_mb': 0, 'cache_dir': str(self.cache_dir)}
