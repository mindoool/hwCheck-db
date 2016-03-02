app.service('storage', [function() {
    this.set = function(key, value) {
        localStorage.setItem(key, JSON.stringify(value));
    };

    this.get = function(key) {
        return JSON.parse(localStorage.getItem(key));
    };

    this.delete = function(key) {
        return localStorage.removeItem('token');
    }
}]);