% rebase("base.tpl", title="Prijava")

<h1>Prijava</h1>
<div class="card bg-secondary">
  <div class="card-body">
    <form action="/prijava/" method="post">
      <div class="form-group">
        <label for="uporabnisko_ime">Uporabniško ime:</label>
        <input type="text" class="form-control" id="uporabnisko_ime" name="uporabnisko_ime" placeholder="Uporabniško ime" minlength="3" maxlength="15" required>
      </div>
      <div class="form-group">
        <label for="geslo">Geslo:</label>
        <input type="password" class="form-control mb-1" id="geslo" name="geslo" placeholder="Geslo" minlength="5" maxlength="20" required>
      </div>
      % if napaka:
      <div class="alert alert-danger py-1 m-0 fs-6">{{napaka}}</div>
      %end
      <div class="d-grid">
        <button class="btn btn-dark mb-3 mt-1" type="submit">Prijava</button>
      </div>
    </form>
    <label for="registracija">Še nimaš računa? Registriraj se:</label>
    <div class="d-grid">
      <a class="btn btn-dark" href="/registracija/" id="registracija">Registracija</a>
    </div>
  </div>
</div>
