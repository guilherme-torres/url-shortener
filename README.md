# URL Shortener
#### Video Demo:  [https://youtu.be/LxqH-rDGMzY](https://youtu.be/LxqH-rDGMzY)
#### Description:
This project is a URL shortener, a web application where users can register and create short links, and the application shows the number of clicks on each short link created.

#### Technologies:
- Python/Flask
- SQLite
- HTML
- CSS

#### Implementation details:
The application has 7 routes
```
/
```
This is the application's main route, which can only be accessed if the user is logged in. If logged in, the user can create and manage their short links.

```
/login
```
This is the first route accessed when the user enters the application. Its function, as the name implies, is to log the user in. In addition, a new session is created so that the application recognizes the user in the other routes.

```
/logout
```
Clears the user's session and redirects to the `/login` route.

```
/register
```
This route has a form that asks for a username and password to register a new user. The application does not allow users with the same username.
```
/create
```
This route performs the main function of the application, creating short links. Each short link is saved in the database as a sequence of 5 characters, containing uppercase letters, lowercase letters and numbers.

```
/delete/<id>
```
Deletes a short link from the database.

```
/<short>
```
This is the route capable of redirecting a short link to its destination URL. In this route, the `<short>` is replaced by the 5-character ID of the short link. When accessing this route, the click count for this link is incremented in the database.
