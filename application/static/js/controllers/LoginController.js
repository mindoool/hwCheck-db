app.controller('LoginController', ['$scope', '$mdDialog', '$mdMedia', '$http', 'storage', '$state', '$rootScope', 'CommonData', function ($scope, $mdDialog, $mdMedia, $http, storage, $state, $rootScope, CommonData) {
    $scope.commonData = CommonData;

    $scope.user = {
        email: "",
        password: ""
    };

    $scope.login = function () {
        console.log('hi');
        $http.post(host+'/users/login', $scope.user)
            .then(function successCallback(response) {
                storage.set('token', response.data.token);
                storage.set('userData', response.data.data);
                console.log(response.data);
                $scope.$root.token = response.data.token;
                $http.defaults.headers.common.Authorization = storage.get('token');
                $scope.$root.user = response.data.data;
                if (response.data.data.isAdmin) {
                    $state.go('admin');
                } else {
                    $state.go('hwlist');
                }
            }, function errorCallback(response) {
                alert('이메일 주소나 비밀번호가 잘못되었습니다.');
            });
    };

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

        //service에서 가져오기
        $scope.courseGroupObj = $scope.commonData.getCourseGroupObj();
        $scope.selectedCourse = null;
        $scope.targetGroup = 0;

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