app.controller('UserEditController', ['$scope', '$mdDialog', '$mdMedia', '$http', 'storage', '$state', '$rootScope', 'CommonData', function ($scope, $mdDialog, $mdMedia, $http, storage, $state, $rootScope, CommonData) {
    $scope.commonData = CommonData;

    $scope.user = $rootScope.user;

    $scope.groupCourseUserList = [];
    $scope.getUserGroupList = function () {
        var params = {
            userId: $scope.user.id,
            groupId: 0
        };
        $http.get(host + "/user-group-relations", {params: params})
            .then(function (response) {
                $scope.groupCourseUserList = response.data.data;
                console.log($scope.groupCourseUserList);
            });
    };

    $scope.getUserGroupList();

    $scope.courseGroupObj = $scope.commonData.getCourseGroupObj();
    $scope.selectedCourse = null;
    $scope.targetGroup = 0;

    $scope.editUser = function () {
        console.log('hi');
        $http.put(host+'/users/'+$scope.user.id, $scope.user)
            .then(function successCallback(response) {
                storage.set('token', response.data.token);
                $scope.$root.token = response.data.token;
                storage.set('userData', response.data.data);
                $scope.$root.user = response.data.data;
                $http.defaults.headers.common.Authorization = storage.get('token');
                console.log(response.data);
                if (response.data.data.isAdmin) {
                    $state.go('admin');
                } else {
                    $state.go('hwlist');
                }
            }, function errorCallback() {
                alert('회원 정보를 바꿀 수 없습니다. 내용 확인 후 다시 시도해 보세요.');
            });
    };
}]);