(function(exports) {
  var parseJWT = function(jwt) {
    var payload = jwt.split(".")[1];
    payload = JSON.parse(atob(payload));
    if (!!payload.d) {
      // old format
      payload = payload.d;
    } else {
      // new format
      var username = payload.uid;
      payload = payload.claims;
      payload.uid = username;
    }
    return {
      token: jwt,
      name: payload.name,
      group: payload.group,
      email: payload.email,
      username: payload.uid
    }
  };
  var getRosefireToken = function(registryToken, callback) {
    var token = encodeURIComponent(registryToken);
    var origin = encodeURIComponent(location.origin);
    var rosefireWindow = window.open('https://rosefire.csse.rose-hulman.edu/webview/login?platform=web&registryToken=' + token + '&referrer=' + origin, '_blank');
    // Hacky, but seems to be the only method.
    var intervalId = setInterval(function() {
      if (rosefireWindow.closed) {
          clearInterval(intervalId);
          if (callback) {
            callback(new Error('Login cancelled'));
            callback = null;
          }
      }
    }, 500);
    window.addEventListener('message', function(event) {
      var origin = event.origin || event.originalEvent.origin;
      if (origin !== 'https://rosefire.csse.rose-hulman.edu') {
        console.error('Invalid origin:' + origin);
        return;
      }
      var cb = callback;
      callback = null;
      clearInterval(intervalId);
      event.source.close();
      if (cb) {
        cb(null, parseJWT(event.data));                     
      }
    });
  };
  exports.Rosefire = {};
  exports.Rosefire.signIn = getRosefireToken;
})(this);
