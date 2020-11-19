import cProfile 
import ProfileSingleFrame 

cProfile.run('ProfileSingleFrame.showVideo()')


"""
 Ordered by: standard name

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    3.512    3.512 <string>:1(<module>)
        1    0.028    0.028    3.512    3.512 ProfileSingleFrame.py:33(showVideo)
      100    0.000    0.000    0.001    0.000 base64.py:34(_bytes_from_decode_data)
      100    0.001    0.000    0.052    0.001 base64.py:51(b64encode)
      100    0.000    0.000    0.073    0.001 base64.py:65(b64decode)
      100    0.002    0.000    0.002    0.000 queue.py:110(full)
      100    0.002    0.000    0.004    0.000 queue.py:121(put)
      200    0.000    0.000    0.001    0.000 queue.py:208(_qsize)
      100    0.000    0.000    0.000    0.000 queue.py:212(_put)
      100    0.000    0.000    0.000    0.000 threading.py:246(__enter__)
      100    0.000    0.000    0.000    0.000 threading.py:249(__exit__)
      100    0.001    0.000    0.001    0.000 threading.py:261(_is_owned)
      100    0.001    0.000    0.002    0.000 threading.py:341(notify)
      100    0.072    0.001    0.072    0.001 {built-in method binascii.a2b_base64}
      100    0.052    0.001    0.052    0.001 {built-in method binascii.b2a_base64}
        1    0.000    0.000    3.512    3.512 {built-in method builtins.exec}
      200    0.000    0.000    0.000    0.000 {built-in method builtins.isinstance}
      200    0.000    0.000    0.000    0.000 {built-in method builtins.len}
      101    0.032    0.000    0.032    0.000 {built-in method builtins.print}
      100    0.002    0.000    0.002    0.000 {built-in method numpy.frombuffer}
      101    0.000    0.000    0.000    0.000 {built-in method time.time}
      100    1.064    0.011    1.064    0.011 {imdecode}
      100    1.418    0.014    1.418    0.014 {imencode}
      100    0.000    0.000    0.000    0.000 {method '__enter__' of '_thread.lock' objects}
      100    0.000    0.000    0.000    0.000 {method '__exit__' of '_thread.lock' objects}
      100    0.000    0.000    0.000    0.000 {method 'acquire' of '_thread.lock' objects}
      100    0.000    0.000    0.000    0.000 {method 'append' of 'collections.deque' objects}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
      100    0.835    0.008    0.835    0.008 {method 'read' of 'cv2.VideoCapture' objects}
"""