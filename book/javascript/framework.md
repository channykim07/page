# Framework

> Framework vs Library 

* Framework is a piece of code that dictates the architecture of your project and aids in programs
* pre-written JavaScript which allows for easier development of JavaScript-based applications

## Jquery

* introduces css-like syntax and several visual and UI enhancements 
* simplifies the use of Javascript in websites 
* an abstraction of the core language

### Syntax

> Install

```html
// check jQuery version
// console.log(jQuery.fn.jquery)
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1/jquery.js"></script>
```

> Variable

```js
const $a = $('#id');        // variable starts with $
const $b = $('.classname')
$('element:hidden/visible')              // Matches all elements that are hidden / visible
$('#container').children(':visible');    // Get visible children
```

* each()

```js
$( "li" ).each(function( index ) {
  console.log( index + ": " + $( this ).text() );
});
```

> Error

* Uncaught TypeError: Cannot read property 'call' of undefined
  * each() requires a handler use on() instead

## Vue

* model–view–viewmodel front end JavaScript framework for building user interfaces and single-page applications.

## React

### Material UI

* Explicitly built for react
* Flexibility, customize than bootstrap and semantic UI
* Active development, hooks

### Native

* Crossplatform application

```sh
npm i -g create-react-native-app
create-react-native-app my-project
cd my-project
npm start
yarn add react-native-elements
```

### Expo

> Lan

* For this to work, on the same wifi network as your computer
* Fastest, safest. The phone connects to your computer just through your router.

> Tunnel 

* Under tunnel setting, your computer will setup a tunnel to exp.direct, 
* a domain using the ngrok tunnel service. 
* all traffic will go through a proxy in the cloud, but it can punch through most firewalls, 
* it will work under more conditions.

> download

```
npm install -g expo-cli
expo init my-new-project
cd my-new-project
expo start
npm run eject    # removes the app from the Expo framework
```