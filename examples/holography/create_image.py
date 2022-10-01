from lmrtfy.functions import catalog

job = catalog.simulate_holography(5, 1023)


if job:
    old_status = job.status
    print(f"status => {old_status}")
    while not job.ready:
        new_status = job.status
        if new_status != old_status:
            print(f"status => {new_status}")
            old_status = new_status

        import time
        time.sleep(0.1)

    print(job.ready)

