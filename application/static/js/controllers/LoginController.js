app.controller('LoginController', ['$scope', '$mdDialog', '$mdMedia', '$http', 'storage', '$state', '$rootScope', function ($scope, $mdDialog, $mdMedia, $http, storage, $state, $rootScope) {
    $scope.data = [];

    $scope.user = {
        email: "",
        password: ""
    };

    $scope.login = function () {
        console.log('hi');
        $http.post(host+'/users/login', $scope.user)
            .then(function (response) {
                storage.set('token', response.data.token);
                storage.set('userData', response.data.data);
                console.log(response.data);
                $scope.$root.token = response.data.token;
                $http.defaults.headers.common.Authorization = storage.get('token');
                $scope.$root.user = response.data.data;
                if (response.data.data.isAdmin) {
                    $state.go('admin');
                } else {
                    $state.go('index');
                }


            });
    };


    $scope.groupList = [];

    $scope.selectedCourse = null;
    $scope.targetGroup = 0;
    $scope.courseObj = {};


    //group 불러오기
    $http.get(host + "/courses/0/groups", {cache: true})
        .then(function (response) {
            console.log(response);
            $scope.groupList = response.data.data;
            for (var i = 0; i < $scope.groupList.length; i++) {
                var course = $scope.groupList[i].course;

                if (typeof $scope.courseObj[course.id]=="undefined") {
                    course.groups = [$scope.groupList[i]];
                    $scope.courseObj[course.id] = course;
                } else {
                    $scope.courseObj[course.id].groups.push($scope.groupList[i]);
                }
            }
            console.log($scope.courseObj);
        });


    //과제를 출제하기 위해 호출하는 함수
    $scope.signupDialog = function (event) {
        $mdDialog.show({
            controller: SignupController,
            templateUrl: 'templates/signup.html',
            parent: angular.element(document.body),
            targetEvent: event,
            clickOutsideToClose: true,
            fullscreen: true,
            scope: $scope,
            preserveScope : true
        })
    };

    function SignupController($scope, $mdDialog) {
        $scope.hide = function () {
            $mdDialog.hide();
        };
        $scope.cancel = function () {
            $mdDialog.cancel();
        };
        $scope.answer = function () {
            $mdDialog.hide(answer);
        };

        $scope.user = {
            email:"",
            password:"",
            passwordCheck:"",
            name:""
        };

        //$scope.getGroupId = function(id) {
        //    console.log(id);
        //    $scope.user.groupId = id
        //};

        $scope.signup = function () {
            var userData = {
                email: $scope.user.email,
                password: $scope.user.password,
                name: $scope.user.name,
                groupId: $scope.targetGroup
            };
            console.log($scope.user.groupId);
            $http.post(host+'/users', userData)
                .then(function(response) {
                    console.log(response);
                    $scope.hide()
                })
        }
    }
}]);