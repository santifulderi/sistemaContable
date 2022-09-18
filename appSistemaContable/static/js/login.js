let working = false;

$('.login').on('submit', function(e) {
    e.preventDefault();
    if (working) return;
    working = true;
    let $this = $(this),
        $state = $this.find('button > .state');
    $this.addClass('cargando');
    $state.html('Autenticando');
    setTimeout(function() {
        $this.addClass('ok');
        $state.html('Bienvenido de nuevo!');
        setTimeout(function() {
            $state.html('Log in');
            $this.removeClass('ok cargando');
            working = false;
        }, 4000);
    }, 3000);
});