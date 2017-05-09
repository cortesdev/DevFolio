/**
 * AngularJS module that adds support for ui-bootstrap modal states when using ui-router
 *
 * @link https://github.com/nonplus/angular-ui-router-resolve-error#readme
 *
 * @license angular-ui-router-resolve-error v0.0.1
 * (c) Copyright Stepan Riha <github@nonplus.net>
 * License MIT
 */

(function(angular) {

"use strict";
angular.module("ui.router.resolve-error", [])
	.run(["$rootScope", function($rootScope) {

		$rootScope.$on( '$stateChangeError', function (event, toState, toParams, fromState, fromParams, error) {
			if (error.message.match(/\[\$injector:unpr\]/)) {
				// Log missing 'resolve' dependency
				// See: https://github.com/angular-ui/ui-router/issues/469
				console && console.error("Invalid resolve in state '" + toState.name + "' - " + error.message);
			}
		});

	}]);


})(window.angular);