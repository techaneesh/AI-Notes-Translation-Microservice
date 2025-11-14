from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from django.core.cache import cache
from django_redis import get_redis_connection
from notes.models import Note

@api_view(['GET'])
def stats_view(request):
    """
    Analytics endpoint that returns:
    - Total number of notes
    - Count of translations performed
    - Breakdown by original language
    """
    # Total number of notes
    total_notes = Note.objects.count()
    
    # Count of translations performed (notes that have translated_text)
    translations_count = Note.objects.filter(
        translated_text__isnull=False
    ).exclude(translated_text='').count()
    
    # Breakdown by original language
    language_breakdown = Note.objects.values('original_language').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Format the language breakdown as a dictionary
    language_stats = {
        item['original_language']: item['count']
        for item in language_breakdown
    }
    
    # Prepare response data
    response_data = {
        'total_notes': total_notes,
        'translations_count': translations_count,
        'breakdown_by_language': language_stats
    }
    
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
def cache_info_view(request):
    """
    Demonstration endpoint to show Redis cache is being used
    Returns cache statistics and sample cache keys
    """
    try:
        # Get Redis connection
        redis_conn = get_redis_connection("default")
        
        # Get cache info
        cache_info = {
            'redis_connected': True,
            'cache_backend': 'django_redis.cache.RedisCache',
            'redis_server_info': redis_conn.info('server'),
        }
        
        # Get all cache keys (sample)
        try:
            # Get keys with our prefix
            all_keys = redis_conn.keys('notes_cache:*')
            cache_keys_sample = [key.decode('utf-8') for key in all_keys[:10]]  # First 10 keys
            
            cache_info['total_cache_keys'] = len(all_keys)
            cache_info['sample_cache_keys'] = cache_keys_sample
        except Exception as e:
            cache_info['cache_keys_error'] = str(e)
        
        # Test cache operations
        test_key = 'notes_cache:test_demo_key'
        test_value = 'Redis is working!'
        cache.set(test_key, test_value, 60)  # Cache for 60 seconds
        retrieved_value = cache.get(test_key)
        
        cache_info['cache_test'] = {
            'test_key': test_key,
            'test_value_set': test_value,
            'test_value_retrieved': retrieved_value,
            'test_passed': retrieved_value == test_value
        }
        
        # Get some cache statistics
        try:
            cache_info['redis_stats'] = {
                'connected_clients': redis_conn.info('clients').get('connected_clients', 'N/A'),
                'used_memory_human': redis_conn.info('memory').get('used_memory_human', 'N/A'),
                'total_keys': redis_conn.dbsize(),
            }
        except Exception as e:
            cache_info['redis_stats_error'] = str(e)
        
        return Response({
            'message': 'Redis cache is active and working!',
            'cache_info': cache_info
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': 'Failed to connect to Redis',
            'details': str(e),
            'message': 'Redis may not be running or configured correctly'
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
