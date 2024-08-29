[![codecov](https://codecov.io/gh/David-Brierley/APIClientBase/graph/badge.svg?token=G5X3AEA52D)](https://codecov.io/gh/David-Brierley/APIClientBase)
![Lint and Format](https://github.com/David-Brierley/APIClientBase/actions/workflows/lint.yml/badge.svg)

![image](https://github.com/user-attachments/assets/59fe1fd9-1534-4f0e-95bf-ac13d51403b7)


# API Client Base 
A simple api client package built using an abstract base class.
Extendable for specific implementations using subclasses to implement api specific logic.

## Background
Create originally to explore rewriting a 'standard class' I had for consuming an API and making use of Abstract Base Classes.
This excersize also allowed me to experiment more with GitHub as opposed to GitLab.


## Install
~~install using pip `pip install api_client_base`~~

*note*: currently not installable on pip.

instead either use directly or like so

```
git clone https://github.com/David-Brierley/APIClientBase.git
cd APIClientBase/
poetry install
```

The project should install
Then start a venv using `poetry shell`

And you will see the package installed as editable like so

```
pip list
...
Package            Version  Editable project location
------------------ -------- --------------------------------
api_client_base    0.1.0    /your/dir/APIClientBase

```



## Implementations
The following have been implemented and are included in the package.

### Logicmonitor
An api client to interface with the logicmonitor API.
The auth logic of the Logicmonitor API is somewhat unique in that a signature must be generated for each request.
The subclass takes care of this behind the scenes to prevent having to clutter code with the auth logic.
This has been implemented using a decorator function to keep the code simple.

### basic_api_token
An very very basic implementation of a subclass which can be used to interface with a generic API using 'static token in the header auth'.

## Pagination
A seperate base class has been created to handle pagination.
The subclasses can inherrit this through multiple inheritence.
Pagination logic should be implemented in a subclass.

The idea is an api should follow the same pagination logic throughout.
Should be able to call all / request all on a GET request without needing to paginate in your script.

### Pagination implementations
A simple offset implementation has been created and allows for pagination using offset and size as query parameters.
Other implementations can be created.

Subclasses do not have to inherrit from the Pagination class if they don't want or need to.

## Creating a new subclass
The designed use of the base class is.

* must accept base URL
* must allow providing the path to send the requests to
* must allow query params
* must allow payload to be sent
* must allow custom headers

This covers most consumeable rest API's functionality requirements.

Furthermore each subclass must implement at the very minimum the abstract methods.
The methods are detailed bellow.


### Abstract methods
| **Method**   | **Arguments**                               | **Description**                                           |
|--------------|---------------------------------------------|-----------------------------------------------------------|
| `get`        | `path: str, **kwargs`                       | Abstract method for sending a GET request to the API.     |
| `post`       | `path: str, **kwargs`                       | Abstract method for sending a POST request to the API.    |
| `put`        | `path: str, **kwargs`                       | Abstract method for sending a PUT request to the API.     |
| `patch`      | `path: str, **kwargs`                       | Abstract method for sending a PATCH request to the API.   |
| `delete`     | `path: str, **kwargs`                       | Abstract method for sending a DELETE request to the API.  |
| `update_headers` | `headers: dict`                         | Abstract method for updating the request headers.         |


### Headers
The baseclass only enforces 2 headers.
```
{
    "Content-Type": "application/json",
    "Accept": "application/json",
}
```

Any additional required headers can be added using the `update_headers` method. A call to this method will *update* the headers, essentially adding to if you do not provide the original keys.

### Helper methods
The following helper / wrapper methods exist.
These methods essentially facillitate the most common form of the HTTM Methods (GET, POST, PATCH, PUT & DELETE) by using the requests library.

| **Method**      | **Arguments**             | **Description**                                                                 |
|-----------------|---------------------------|---------------------------------------------------------------------------------|
| `common_get`    | `path: str, **kwargs`     | Wrapper method that internally calls `_make_request` with the GET method.       |
| `common_post`   | `path: str, **kwargs`     | Wrapper method that internally calls `_make_request` with the POST method.      |
| `common_put`    | `path: str, **kwargs`     | Wrapper method that internally calls `_make_request` with the PUT method.       |
| `common_patch`  | `path: str, **kwargs`     | Wrapper method that internally calls `_make_request` with the PATCH method.     |
| `common_delete` | `path: str, **kwargs`     | Wrapper method that internally calls `_make_request` with the DELETE method.    |
| `_make_request` | `method: str, path: str, **kwargs` | Helper method that constructs and sends the HTTP request based on the given method, URL, headers, and additional parameters. |

These methods do not have to be used in subclass implementations but are there for conveieance as they cover most common cases.
E.g. it is entirely feaseable to implement the GET, POST etc. using a differnt library if needed.

### Base URL
The base URL is not stricly formatted. Its a simple regex allowing anything which is using https only. This allows for base urls to be localhost / IP addresses / custom ports without the need to verify it.

## Examples
Examples are provided in the examples directory for each implementation.
