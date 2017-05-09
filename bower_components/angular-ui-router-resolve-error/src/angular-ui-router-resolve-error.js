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
