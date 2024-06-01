## Simple Python Application for ACP 2025

### How to get it running:

1. Clone the repository
2. Ensure Docker is running on your machine.
3. `cd` into the repository.
4. Run `docker build . -t acp_py_image`
5. Run `docker run -p 8080:8080 acp_py_image`. This should start the docker container and the application should be accessible.
6. Send requests to the endpoint using your favourite tool (Postman, curl, etc).

### How it works:

This is a quick tour around the code and what does what. I have included some helpful links if you want to dive deeper. 

We are creating our application using the [application factory](https://flask.palletsprojects.com/en/3.0.x/patterns/appfactories/) pattern that Flask provides. This way we can create multiple Blueprints (similar to controllers in spring) and register these with the app to keep it modular while keeping everything nice and neat. 

Within our `simple_blueprint.py` file, we have a simple blueprint with some endpoints that we can hit. 

- `is_alive` - Checks if the application is up and running (recommended as a quick health check).
- `test_path_variable`- Uses a path variable via GET returns the path variable back to you.
- `test_post_with_body` - Uses some JSON POSTed to the endpoint to create a new resource. 
- `test_get_with_query` - Uses query parameters to return a message, [we could also use POST](https://stackoverflow.com/questions/611906/http-post-with-url-query-parameters-good-idea-or-not) with query parameters, but since our endpoint is idempotent (we can make the same request again and again, nothing changes server side), we use GET.
- `get_restaurants` - Will return a list of restaurants in the response body. An example of what a response can look like to requests asking for data. 

Note: These are the functions that are being called and not the endpoints themselves, the endpoints are defined in the `@bp.route()` decorator.

### The Dockerfile

The Dockerfile dictates to docker what needs to be done to create our image. The comments should guide you through what is happening at each step.

```dockerfile
# Using a slim version of python to keep the image size as small as we can.
FROM --platform=linux/amd64 python:3.10.13-slim

# Expose the port in the container that we want to use to access the application, we will still need to map this port
# to a port on our host machine when we run the container.
EXPOSE 8080

# Set the working directory in the container to /app
WORKDIR /app

# Copy the requirements and install them.
COPY ./requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt

# Copy the source code into the container.
COPY ./acptutorialpy ./acptutorialpy

# Tell flask where to find the factory that creates the app.
ENV FLASK_APP=acptutorialpy:create_app

# Run the application when the container starts. We set the host to 0.0.0.0 as flask automatically binds to localhost, this
# doesn't work in our case as the containers network is different to the network on the host machine. So setting the application
# to accept all traffic no matter the IP allows us to access and use the application! Of course we also need to set the port to 8080
# as this is the port we exposed in the Dockerfile.
CMD [ "flask", "run", "--host=0.0.0.0", "--port=8080" ]
```