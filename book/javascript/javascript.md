# Javascript

* interpreted, dynamic typing, prototype-based programming language 

## Speed Optimization
* https://developers.google.com/speed/pagespeed/insights/
* https://tinyjpg.com
* https://jakearchibald.github.io/svgomg/

## Terms

> Versions

* ES5
    * ECMAScript5 developed in 2009
    * Fully supported in all modern browsers

* ES6
    * ECMAScript 2015
    * Internet Explorer does not support ECMAScript 2015
    * let and const, default parameter values, Array.find(), Array.findIndex().

> Packages

```sh
nodemon         # update refresh backend
npm init        # create package.json
npm audit fix   # Scan project install any compatible updates to vulnerable dependencies
npm run rename  # change project name
```

* Start the development server

```sh
npm start
npm list -g
npm root -g
```

> Ajax
* Asynchronous JavaScript and XML
* the request are sent to the server by using XMLHttpRequest objects

> Content delivery network (CDN)

> Status Messages

* 1** Informational      # received and the process is continuing.

```
101 Switching Protocols  # asked the server to switch protocols
103 Checkpoint           # resumable requests proposal to resume aborted PUT/POST requests

# 2xx: Successful       # Message:  Description:
200 OK                  # OK (standard response for successful HTTP requests)
201 Created             # fulfilled, and a new resource is created 
202 Accepted            # accepted for processing, but the processing has not been completed
203 NoAuth Information  # successfully processed, but returning info from another source
204 No Content          # successfully processed, no content
205 Reset Content       # successfully processed, no content, requires that requester reset view
206 Partial Content     # delivering only part of resource due to a range header sent by client

# 3** Redirection       # further action must be taken in order to complete the request.
300 Multiple Choices    # link list. users can select, visit the link. Maximum five addresses  
301 Moved Permanently   # moved to a new URL 
302 Found               # moved temporarily to a new URL 
303 See Other           # page can be found under a different URL
304 Not Modified        # Indicates requested page has not been modified since last requested
306 Switch Proxy        # No longer used
307 Temporary Redirect  # moved temporarily to a new URL
308 Resume Incomplete   # resumable requests proposal to resume aborted PUT/POST requests

# 4** Client Error      # indicates that requested resource is not available at the web server
400 Bad Request         # cannot be fulfilled due to bad syntax
401 Unauthorized        # legal request, but authentication has failed or not yet been provided
402 Payment Required    # Reserved for future use
403 Forbidden           # legal request, but the server is refusing to respond to it
404 Not Found           # not be found but may be available again in the future
405 Method Not Allowed  # made of a page using a request method not supported by that page
406 Not Acceptable      # only generate a response that is not accepted by the client
407 Proxy Auth Required # client must first authenticate itself with the proxy
408 Request Timeout     # server timed out waiting for the request
409 Conflict            # could not be completed because of a conflict in the request
410 Gone                # page is no longer available
411 Length Required     # "Content-Length" is not defined. server requires it
412 Precondition Failed # precondition given in request evaluated to false by server
413 Request Entity Large  # server will not accept request, because request entity is large
414 Request-URI Too Long  # server will not accept request, because URL is too long (GET)
415 Unsupported Media     # server will not accept request, because media type is not supported 
416 Requested Range Not   # asked for a portion of file, but server cannot supply that portion
417 Expectation Failed    # server cannot meet the requirements of Expect request-header field

# 5xx: Server Error       # processing fails due to some unanticipated incident on the server side.
500 Internal Server Error # A generic error, given when no more specific message is suitable
501 Not Implemented       # server either doesn’t recognize request method, or lacks ability to fulfill
502 Bad Gateway           # gateway server received an invalid response from upstream server
503 Service Unavailable   # server is currently unavailable (overloaded or down)
504 Gateway Timeout       # gateway server didn’t receive a timely response from upstream server
505 HTTP Version Not      # does not support the HTTP protocol version used in the request
511 Network Auth          # client needs to authenticate to gain network access
```

> xml

* Extensible Markup Language 
* a markup language that defines a set of rules for encoding documents in a format that is both human-readable and machine-readable

> Application Programming Interface (API)

* a software intermediary that enables two applications to communicate with each other
* All Web services are APIs but not all APIs are Web services
* All Web services need a network to operate while APIs don’t need a network for operation
* First estimate your usage and understand how that will impact the overall cost of the offering
* Many protocols are now available to be used in API testing (ex JMS, REST, HTTP, UDDI and SOAP)

> Representational State Transfer

* an architectural style for developing web services which exploit the ubiquity of HTTP protocol and uses HTTP method to define actions

> Websocket

* two way communication between the clients and the servers
* Four main events : Open / Close / Error / Message

> Same Origin Policy

* When using XMLHttpRequest or Fetch API → local files origin is null

> URI

* stands for Uniform Resource Identifier. It is a string of characters designed for unambiguous identification of resources and extensibility via the URI scheme.

> xss

* Cross Site Scripting
* By using Cross Site Scripting (XSS) technique, users executed malicious scripts (also called payloads) unintentionally by clicking on untrusted links and hence, these scripts pass cookies information to attackers

> HTTP Methods

* GET
    * can be cached, bookmarked, only used to request data (not modify)
    * remain in the browser history, have max 2048 characters, ASCII characters allowed
    * should never be used when dealing with sensitive data
    * application/x-www-form-urlencoded

* POST
    * send data to a server to create/update a resource
    * never cached, do not remain in the browser history, cannot be bookmarked
    * no restrictions on data length
    * application/x-www-form-urlencoded or multipart/form-data / multipart encoding for binary data

* PUT
    * send data to a server to create/update a resource (idempotent to POST)
    * same PUT request multiple times will always produce the same result

* HEAD
    * almost identical to GET, but without the response body

* DELETE
    * DELETE method deletes the specified resource.

* PATCH

* OPTIONS
    * describes the communication options for the target resource.

## Files

> robot.txt

* give rules on how site can be crawled
* links to sitemap

> sitemap.xml

* Informs search engines of the site structures
* provides some meta information about individual pages

> Error

* Maximum update depth exceeded error

```jsx
// pass function or use arrow function instead of calling it
{<td><span onClick={this.toggle()}>Details</span></td>}
{<td><span onClick={this.toggle}>Details</span></td>}
```

* Refused to apply style from 'https://cdn.jsdelivr.net/npm/instantsearch.js' because its MIME type ('application/javascript') is not a supported stylesheet MIME type, and strict MIME checking is enabled.

```html
<link rel="stylesheet" href="styles.css"\>
```

* Uncaught SyntaxError: Cannot use import statement outside a module`

```html
<script type="module" src="../src/main.js"></script>
```

* (node:32660) UnhandledPromiseRejectionWarning: Unhandled promise rejection. This error originated either by throwing inside of an async function without a catch block, or by rejecting a promise which was not handled with .catch(). To terminate the node process on unhandled promise rejection, use the CLI flag `--unhandled-rejections=strict` (see https://nodejs.org/api/cli.html#cli_unhandled_rejections_mode). (rejection id: 1)  
* (node:32660) [DEP0018] DeprecationWarning: Unhandled promise rejections are deprecated. In the future, promise rejections that are not handled will terminate the Node.js process with a non-zero exit code.
  * Do not throw again in catch which is uncaught
  * Do not trust auto import, from sequelize.types -> from sequelize
  * await async function that throws an error

## HTML


## CSS

* describes how HTML elements should be displayed.

> Terms

* id
  * id must start with letters only have one id

* Selector

```js
*             // all elements
div           // all div tags
div, p        // all divs and paragraphs
div p         // paragraphs inside divs

.classname    // all elements with class
#idname       // element with ID
div.classname // divs with certain classname
div#idname    // div with certain ID
#idname *     // all elements inside #idname

[attribute="value"]     // used to select elements with a specified attribute
[attribute~="value"]    // used to select elements with an attribute value containing a specified word
```

* Combinators
  * something that explains the relationship between the selectors

```js
div p             // all elements that are descendants of a specified element
div > p           // all p tags, one level deep in div
div + p           // p tags immediately after div
div ~ p           // p tags preceded by div
```

* unit

```js
// fixed units
cm / mm / in      // centimeters / millimeters / inches (1in = 96px = 2.54cm)
p                 // relative to the viewing device. For high res, 1px = 1+ device pixel
pt / pc           // points (1pt = 1/72 of 1in), picas (1pc = 12 pt)

// Relative Lengths
em                // Relative to font-size of element (2em = x2 of current font)    
ex                // Relative to x-height of current font (rarely used)    
ch                // Relative to width of the "0" (zero)    
rem               // Relative to font-size of the root element    
vw / vh           // Relative to 1% of the width / height of the viewport*    
vmin / vmax       // Relative to 1% of viewport* smaller / larger  dimension    
%                 // Relative to the parent element
```

* z-index
  * only works on positioned elements (position: absolute, relative, fixed, sticky).
  * z-index: auto|number|initial|inherit;

```js
auto (default)    // stack order equal to its parents
number            // stack order of the element. Negative numbers are allowed
```

* visibility

```js
visible       // visible, defaul>
hidden        // hidden (but still takes up space)    
collapse      // Only for <tr>, <tbody>, <col>, <colgroup>. removes a row or column
```

* check hidden

```js
child.offsetWidth > 0 && child.offsetHeight > 0 // also check if parent is hidden
object.style['display'] != 'none'               // only checks the element
```

## HTML

* Hyper Text Markup Language where W3 Consortium is main international standards organization
* request and response protocol.
* media independent protocol.
* stateless protocol.
 
> Term

* global atrribute

```sh
accesskey       # a shortcut key to activate/focus an element
class           # one or more classnames for an element (refers to a class in a style sheet)
contenteditable # Specifies whether the content of an element is editable or not
data-*          # Used to store custom data private to the page or application
dir             # text direction for the content in an element
draggable       # whether an element is draggable or not
hidden          # Specifies that an element is not yet, or is no longer, relevant
id              # Specifies a unique id for an element
lang            # Specifies the language of the element's content
spellcheck      # whether element is to have its spelling and grammar checked or not
style           # an inline CSS style for an element
tabindex        # tabbing order of an element
title           # extra information about an element
translate       # whether the content of an element should be translated or not
```

 ![alt](images/20210210_182233.png)

## Event

```sh
onchange        # HTML element has been changed
onclick         # clicks an HTML element
onmouseover     # moves the mouse over an HTML element
onmouseout      # moves the mouse away from an HTML element
onkeydown       # pushes a keyboard key
onload          # browser has finished loading the page
```

* custom event

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Creating Events</title>
  <meta name="viewport" content="width=device-width">
</head>
<body>
  <h1>Creating Events</h1>
  <main>
  </main>
  <script>
    //1. let evt = new Event('explode');
    //2. let evt = new CustomEvent('explode', {detail:{speed:20, volume:40}});
    let born = new Event('born');
    let died = new CustomEvent('died', {detail:{time:Date.now()}});
    
    document.addEventListener('DOMContentLoaded', function (){
      let m = document.querySelector('main');
      addParagraph(m, 'This is a paragraph.');
      addParagraph(m, 'A new Star Wars movie is coming soon.');
      m.addEventListener('click', function(ev){ removeParagraph(m, m.firstElementChild); })
    });
    
    function addParagraph(parent, txt){
      let p = document.createElement('p');
      p.textContent = txt;
      //set up and dispatch events
      p.addEventListener('born', wasBorn);
      p.addEventListener('died', hasDied);
      p.dispatchEvent(born)
      parent.appendChild(p); //add to screen
    }
    function removeParagraph(parent, p){
      p.dispatchEvent(died); // dispatch event
      parent.removeChild(p); //remove element from screen
    }
    function wasBorn(ev){
      console.log(ev.type, ev.target);
    }
    function hasDied(ev){
      console.log(ev.type, ev.target, ev.detail.time);
      //remove the listeners
      ev.target.removeEventListener('born', wasBorn);
      ev.target.removeEventListener('died', hasDied);
    }
  </script>
</body>
</html>
```

* slider

```js
<style>
  .switch {
    position: relative;
    display: inline-block;
    width: 60px;
    height: 34px;
  }

  .switch input {
    opacity: 0;
    width: 0;
    height: 0;
  }

  /* Square slider */
  .slider {
    position: absolute;
    cursor: pointer;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: #ccc;
    -webkit-transition: .4s;
    transition: .4s;
  }

  .slider:before {
    position: absolute;
    content: "";
    height: 26px;
    width: 26px;
    left: 4px;
    bottom: 4px;
    background-color: white;
    -webkit-transition: .4s;
    transition: .4s;
  }

  input:checked+.slider {
    background-color: #2196F3;
  }

  input:focus+.slider {
    box-shadow: 0 0 1px #2196F3;
  }

  input:checked+.slider:before {
    -webkit-transform: translateX(26px);
    -ms-transform: translateX(26px);
    transform: translateX(26px);
  }

  /* Rounded sliders */
  .slider.round {
    border-radius: 34px;
  }

  .slider.round:before {
    border-radius: 50%;
  }
</style>
<label class="switch">
  <input type="checkbox">
  <span class="slider"></span>
</label>

<label class="switch">
  <input type="checkbox">
  <span class="slider round"></span>
</label>
```

* progress bar

```js
<!DOCTYPE html>
<html>
<style>
  #myProgress {
    width: 100%;
    background-color: #ddd;
  }

  #myBar {
    width: 10%;
    height: 30px;
    background-color: #4CAF50;
    text-align: center;
    line-height: 30px;
    color: white;
  }
</style>

<body>
  <h1>JavaScript Progress Bar</h1>

  <div id="myProgress">
    <div id="myBar">10%</div>
  </div>

  <br>
  <button onclick="move()">Click Me</button>

  <script>
    var i = 0;
    function move() {
      if (i == 0) {
        i = 1;
        var elem = document.getElementById("myBar");
        var width = 10;
        var id = setInterval(frame, 10);
        function frame() {
          if (width >= 100) {
            clearInterval(id);
            i = 0;
          } else {
            width++;
            elem.style.width = width + "%";
            elem.innerHTML = width + "%";
          }
        }
      }
    }
  </script>

</body>

</html>
```

# CSS

> Basic Styles

```js
<link rel="stylesheet" type="text/css" href="theme.css">
```