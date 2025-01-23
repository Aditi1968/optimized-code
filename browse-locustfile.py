from locust import task, run_single_user, FastHttpUser


class Browse(FastHttpUser):
    host = "http://localhost:5000"
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
        Simulates a user browsing the '/browse' endpoint.
        """
        with self.client.get(
            "/browse",
            headers={
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
                "Priority": "u=0, i",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "cross-site",
                "Upgrade-Insecure-Requests": "1",
            },
            catch_response=True,
            name="/browse",
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Failed with status code {response.status_code}")

    def on_start(self):
        """
        Actions to perform when a user starts the test.
        """
        print(f"User started: {self.host}")

    def on_stop(self):
        """
        Actions to perform when a user stops the test.
        """
        print(f"User stopped: {self.host}")


if __name__ == "__main__":
    run_single_user(Browse)
