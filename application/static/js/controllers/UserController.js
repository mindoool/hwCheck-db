app.controller('UserController', ['$scope', 'storage', '$mdMedia', '$mdDialog', '$http', '$filter', 'CommonData', function ($scope, storage, $mdMedia, $mdDialog, $http, $filter, CommonData) {

    //userGroup불러오기
    $scope.userGroupList = [];

    $scope.groupList = [];

    $scope.selectedGroup = null;
    $scope.targetGroup = 0;
    $scope.groupObj = {};
    $scope.groupCourseUserList = [];


    $scope.getUserGroupList = function () {
        var params = {
            userId: 0,
            groupId: 0
        };
        $http.get(host + "/user-group-relations", {params: params}, {cache: true})
            .then(function (response) {
                $scope.groupCourseUserList = response.data.data;
                console.log($scope.groupCourseUserList);
            });
    };

    $scope.getUserGroupList();

    //유저의 반을 수정하는 함수
    $scope.editUserDialog = function (event, obj) {
        $mdDialog.show({
            controller: UserController,
            templateUrl: 'templates/edit-user.html',
            parent: angular.element(document.body),
            targetEvent: event,
            clickOutsideToClose: true,
            fullscreen: true,
            scope: $scope,
            preserveScope: true,
            locals: {
                obj: obj
            }
        })
    };

    function UserController($scope, $mdDialog, obj) {
        $scope.hide = function () {
            $mdDialog.hide();
        };
        $scope.cancel = function () {
            $mdDialog.cancel();
        };
        $scope.answer = function (answer) {
            $mdDialog.hide(answer);
        };

        $scope.currentUser = {
            name: obj.name
        };

        $scope.dialogGroupCourseUserObj = obj;

        $scope.selectedCourse = null;
        $scope.targetGroup = 0;
        $scope.courseGroupObj = CommonData.getCourseGroupObj();

        //$scope.getGroup = function () {
        //    $http.get(host + "/courses/" + $scope.dialogGroupCourseUserObj.course.id + "/groups")
        //        .then(function (response) {
        //            console.log(response);
        //            $scope.groupList = response.data.data;
        //        });
        //};
        //
        //$scope.getGroup();

        $scope.editGroupCourseUser = function (user) {
            var userData = {
                userId : user.id,
                groupId: user.selectedGroupId
            };
            $http.put(host + "/user-group-relations/" + user.userGroup.id, userData)
                .then(function (response) {
                    console.log(response);
                    $scope.hide();
                    $scope.getUserGroupList()
                });
        }
    }

}])
;