<!DOCTYPE html>
<html lang="si">
  <head>
    <title>{{title}}</title>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-0evHe/X+R7YkIZDRvuzKMRqM+OrBnVFBL6DOitfPri4tjfHxaWutUpFmBp4vmVor" crossorigin="anonymous">
    
    <!-- Latest compiled and minified CSS -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-select@1.13.14/dist/css/bootstrap-select.min.css">
    <!-- Latest compiled and minified JavaScript -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap-select@1.13.14/dist/js/bootstrap-select.min.js"></script>
    <!-- (Optional) Latest compiled and minified JavaScript translation files -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap-select@1.13.14/dist/js/i18n/defaults-*.min.js"></script>
    
     <!-- jQuery -->
     <script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
    
     <!-- Bootstrap JS -->
     <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.bundle.min.js"></script>
     
     <!-- Bootstrap-Select JS -->
     <script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-select/1.13.18/js/bootstrap-select.min.js"></script>
 
     <script>
         $(document).ready(function () {
             $('.selectpicker').selectpicker();
         });
     </script>

    <link href="/static/style.css" rel="stylesheet">
    <link rel="icon" href="/img/stock.png">
  </head>
  <body class="bg-dark text-light besedilo">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/js/bootstrap.bundle.min.js" integrity="sha384-pprn3073KE6tl6bjs2QrFaJGz5/SUsLqktiwsUTF55Jfv3qYSDhgCecCxMW52nD2" crossorigin="anonymous"></script>
    <div class="row">
      <div class="col">
        <img src="/img/puscice1.svg" alt="puscice1" class="sticky-top float-end invert puscice">
      </div>
      <div class="col-6">
        <nav class="navbar navbar-expand-xl sticky-top bg-dark">
          <div class="container-fluid">
            <a class="navbar-brand text-light besedilo" href="/">
              <img src="/img/stock.png" alt="Pregledovalec portfeljev" height="22em" class="d-inline-block align-text-top">
              Pregledovalec portfeljev
            </a>
            <button class="navbar-toggler btn-outline-light" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
              <span class="navbar-toggler-icon invert"></span>
            </button>
            <div class="collapse navbar-collapse justify-content-between" id="navbarNav">
              <ul class="navbar-nav mr-auto">
                <li class="nav-item dropdown">
                  <a class="nav-link text-light" href="/moji-portfelji/">
                    Moji portfelji
                  </a>
                </li>
                <li class="nav-item">
                  <a class="nav-link text-light" href="/kriptovalute/">
                    Kriptovalute
                  </a>
                </li>
              </ul>
              
              <div class="nav-item">
                % if uporabnisko_ime:
                <a class="nav-link text-light" href="/profil/">{{uporabnisko_ime}}</a>
                % else:
                <a class="nav-link text-light" href="/prijava/">Prijava</a>
                % end
              </div>
             
            </div>
          </div>
        </nav>
        {{!base}}
      </div>
      <div class="col">
        <img src="/img/puscice2.svg" alt="puscice1" class="sticky-top float-start invert puscice">
      </div>
    </div>
  </body>
</html>