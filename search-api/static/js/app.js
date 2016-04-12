'use strict';

// Declare app level module which depends on views, and components
var app = angular.module('myApp', [
  'ngRoute',
  'ngResource',

]).
config(['$routeProvider', '$httpProvider', '$locationProvider', function($routeProvider, $httpProvider, $locationProvider) {

  $routeProvider
    .when('/query/:id', {
       templateUrl: '../static/partials/view1.html',
       controller: 'MainController'
    })
    .otherwise({redirectTo: '/query/1'});

   $httpProvider.defaults.withCredentials = true;
        delete $httpProvider.defaults.headers.common["X-Requested-With"];

  $locationProvider.html5Mode(true);
}]);

app.factory('Api', ['$resource',
    function($resource) {
        return {
            Judgement: $resource('/api/judgement/:id', {id:'@id'}),
            Search: $resource('/api/search'),
            Query: $resource('/api/query/:id', {query:'@id'}, {'get': {method:'GET'}})
        };
}]);

app.controller('MainController', function(Api, $scope, $rootScope, $http, $sce, $routeParams){
  $scope.$sce = $sce;
  $scope.query_id = $routeParams.id;
	$scope.resultsList = [];
 	$scope.loadResults = function(){
        $scope.resultsList = Api.Search.query({query_id:$scope.query_id});
        console.log(JSON.stringify($scope.resultsList));
  }

  $scope.postJudgements = function(){
    console.log($scope.resultsList);
    Api.Judgement.save({id: $scope.query_id}, $scope.resultsList);
  }

})
