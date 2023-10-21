Serial:


serial：['/dev/ttyUSB0', '/dev/ttyUSB1']

main    ->  receive_thread
        ->  send_thread

serial  ->  receive_thread
    
        for  
            try:
                ser.init()
                receive_thread_task_create()
            except FileNotFoundError:
                time.sleep 0.2s

