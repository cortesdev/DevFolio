angular-ui-router-resolve-error
===============================

[![Build Status](https://travis-ci.org/nonplus/angular-ui-router-resolve-error.svg?branch=master)](https://travis-ci.org/nonplus/angular-ui-router-resolve-error)

AngularJS module for logging an error to console when `resolve` does not find dependency to inject.

Motivation
----------

Currently if a `resolve` definition for ui-router [$stateProvider.state()](http://angular-ui.github.io/ui-router/site/#/api/ui.router.state.$stateProvider#methods_state)
incorrectly injects dependencies that do not actually exist, transitioning to that state fails without an error being logged in the console.

```
$stateProvider.state('app', {
  ...
  resolve: {
    someValue: function(MissingDependency) {
      return MissingDependency.getValue();
    }
  }
}):
```

Identifying this mistake can be a pain, especially in minified production code.  See [ui-router issue 369](https://github.com/angular-ui/ui-router/issues/469).

This module catches the problem and logs a useful error to the console:

```error
Invalid resolve in state 'app' - [$injector:unpr] Unknown provider: MissingDependencyProvider <- MissingDependency
```

Installing the Module
---------------------
Installation can be done through bower or npm:

``` shell
bower install angular-ui-router-resolve-error
```

In your page add:
```html
  <script src="bower_components/angular-ui-router-resolve-error/angular-ui-router-resolve-error.js"></script>
```

Loading the Module
------------------

This module declares itself as `ui.router.resolve-error`, so it can be declared as a dependency of your application as normal:

```javascript
var app = angular.module('myApp', ['ng', 'ui.router.resolve-error']);
```

Copyright & License
-------------------

Copyright 2016 Stepan Riha. All Rights Reserved.

This may be redistributed under the MIT licence. For the full license terms, see the LICENSE file which
should be alongside this readme.



