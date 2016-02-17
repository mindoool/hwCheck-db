app.directive('hw', function(){
    return {
        restrict: 'E',
        scope: {
            todo: '='
        },
        templateUrl: 'templates/directives/hw.html'
    };
});