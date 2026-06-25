import time

from fastapi import FastAPI, Request


def register_middleware(app: FastAPI):
    """
    Register application middleware.
    """

    @app.middleware("http")
    async def add_process_time_header(
        request: Request,
        call_next,
    ):
        """
        Measure request processing time.
        """

        # Record the start time
        start_time = time.perf_counter()

        # Process the request
        response = await call_next(request)

        # Record the end time
        end_time = time.perf_counter()

        # Calculate total processing time
        process_time = end_time - start_time

        # Add custom response header
        response.headers["X-Process-Time"] = f"{process_time:.6f} sec"

        # Log to terminal
        print(
            f"{request.method} {request.url.path} - {process_time:.6f} sec"
        )

        return response