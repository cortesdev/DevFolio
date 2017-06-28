var app = angular.module('myApp', ['ngAnimate'], ['ui.bootstrap']);


//myApp.directive('myDirective', function() {});
//myApp.factory('myService', function() {});

function NavBarCtrl($scope) {
    $scope.isCollapsed = true;
}
