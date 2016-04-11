'use strict';

// Declare app level module which depends on views, and components
var app = angular.module('myApp', [
  'ngRoute',
  'ngResource',

]).
config(['$routeProvider', '$httpProvider', function($routeProvider, $httpProvider) {

  $routeProvider.
    when('/', {
       templateUrl: '../static/partials/view1.html',
    })
    .otherwise({redirectTo: '/partials/view1'});

   $httpProvider.defaults.withCredentials = true;
        delete $httpProvider.defaults.headers.common["X-Requested-With"];
}]);

app.factory('Api', ['$resource',
    function($resource) {
        return {
            Search: $resource('/api/search'),
            Query: $resource('/api/query/:id', {query:'@id'}, {'get': {method:'GET'}})
        };
}]);

app.controller('MainController', function(Api, $scope, $rootScope, $http){
	$scope.resultsList = ["hello"];
 	$scope.loadResults = function(){
        $scope.resultsList = Api.Search.query({query_id:22});
        console.log(JSON.stringify($scope.resultsList));
    }

})
