<h1>simple slack django integration</h1>

<h2>step 1:</h2>
install ngrok: brew install ngrok/ngrok/ngrok

add token: ngrok config add-authtoken <token>

start: ngrok http 8000

<h2>step 2:</h2>

register ngrok url with slack event subscription for app_mention:read Oauth with chat:write , commands, files:write and user:read Oauth
<br> url example : https://d373-49-207-207-250.in.ngrok.io/slackmessage/event/

<br> same kind of url should be register for slash commands too
<br> url example: https://d373-49-207-207-250.in.ngrok.io/slackmessage/prev_msgs/ -> for all prev messages
<br> https://4988-49-207-223-230.in.ngrok.io/slackmessage/get_file/ -> for uploading a file


<h1>Start server</h1>
docker-compose up django-dev

<h1> run tests</h1>
docker-compose up django-test --build --abort-on-container-exit --exit-code-from django-test