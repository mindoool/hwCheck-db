app.controller('GroupController', ['$scope', 'storage', '$mdMedia', '$mdDialog', '$http', 'CommonData', function ($scope, storage, $mdMedia, $mdDialog, $http, CommonData) {
    //과정 생성하는 함수

    $scope.groupList = CommonData.getGroupList();

    //$scope.getGroup = function () {
    //    $http.get(host + "/courses/0/groups")
    //        .then(function (response) {
    //            console.log(response);
    //            $scope.groupList = response.data.data;
    //            $scope.commonCourseList = CommonData.getCourseList();
    //        });
    //};
    //
    //$scope.getGroup();

    $scope.createGroupDialog = function (ev) {
        $mdDialog.show({
            controller: GroupDialogController,
            templateUrl: 'templates/create-group.html',
            parent: angular.element(document.body),
            targetEvent: ev,
            clickOutsideToClose: true,
            fullscreen: true,
            scope: $scope,
            preserveScope: true,
            group: ev
        })
    };

    function GroupDialogController($scope, $mdDialog, group) {
        $scope.hide = function () {
            $mdDialog.hide();
        };
        $scope.cancel = function () {
            $mdDialog.cancel();
        };
        $scope.answer = function (answer) {
            $mdDialog.hide(answer);
        };

        //서버로 부터 개별과제 받아오는 http.get이 추가되어야 함
        $scope.group = {
            name: "",
            courseId: ""
        };

        $scope.currentGroup = group;
        console.log(group);

        $http.get(host + "/courses", {cache: true})
            .then(function (response) {
                console.log(response);
                $scope.courseList = response.data.data;
            });

        $scope.createGroup = function () {
            var groupData = {
                name: $scope.group.name
            };
            $http.post(host + '/courses/' + $scope.group.courseId + '/groups', groupData)
                .then(function (response) {
                    console.log(response);
                    $scope.getGroup();
                    $scope.hide();
                })
        };

        $scope.editGroup = function () {
            var groupData = {
                name: $scope.currentGroup.name
            };
            $http.put(host + "/courses/" + $scope.currentGroup.courseId + '/groups/' + $scope.currentGroup.id, groupData)
                .then(function (response) {
                    console.log(response);
                    $scope.getGroup();
                    $scope.hide();
                });
        }
    }


    //과정 수정하는 함수
    $scope.editGroupDialog = function (event, group) {
        $mdDialog.show({
            controller: GroupDialogController,
            templateUrl: 'templates/edit-group.html',
            parent: angular.element(document.body),
            targetEvent: event,
            clickOutsideToClose: true,
            fullscreen: true,
            scope: $scope,
            preserveScope: true,
            locals: {
                group: group
            }
        })
    };


    //과정 삭제
    $scope.deleteGroup = function (group) {
        console.log('delete');
        $http.delete(host + "/courses/" + group.course.id + '/groups/' + group.id)
            .then(function (response) {
                console.log(response);
                $scope.getGroup()
            });
    };


}]);