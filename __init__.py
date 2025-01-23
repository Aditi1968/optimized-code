from locust import task, between, FastHttpUser


class BrowseUser(FastHttpUser):
    """
    Simulates a user browsing the application with optimized requests.
    """
    host = "http://localhost:5000"  # Ensure this matches your application host
    wait_time = between(0.1, 0.5)  # Shorten wait time for more frequent requests
    default_headers = {
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "DNT": "1",
        "Sec-GPC": "1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
    }

    @task
    def browse_page(self):
        """
        Simulates browsing a page by sending a GET request.
        """
        with self.client.get(
            "/browse",
            headers={
                **self.default_headers,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
            },
            catch_response=True,
        ) as response:
            if response.status_code != 200:
                response.failure(f"Failed to load page: {response.status_code}")
            else:
                response.success()

    @task
    def view_product(self):
        """
        Simulates viewing a specific product by sending a GET request.
        """
        product_id = 1  # Replace with dynamic logic or pre-fetch IDs
        with self.client.get(
            f"/product/{product_id}",
            headers=self.default_headers,
            catch_response=True,
        ) as response:
            if response.status_code != 200:
                response.failure(f"Failed to load product {product_id}: {response.status_code}")
            else:
                response.success()

    @task
    def add_to_cart(self):
        """
        Simulates adding a product to the cart with a POST request.
        """
        payload = {"product_id": 1, "quantity": 1}  # Replace with dynamic logic
        with self.client.post(
            "/cart/add",
            json=payload,
            headers={
                **self.default_headers,
                "Content-Type": "application/json",
            },
            catch_response=True,
        ) as response:
            if response.status_code != 200:
                response.failure(f"Failed to add product to cart: {response.status_code}")
            else:
                response.success()


if __name__ == "__main__":
    import os
    from locust import run_single_user

    os.environ["LOCUST_LOGLEVEL"] = "ERROR"  # Suppress verbose logs for performance
    run_single_user(BrowseUser)
