% rebase("base.tpl", title="Profil" + uporabnisko_ime)

<h1>Profil uporabnika {{uporabnisko_ime}}</h1>
<div class="card bg-secondary mb-3">
  <div class="card-header fs-3">
    Pregled statistike
  </div>
  <div class="card-body pt-1">
    <p>
      Tu lahko dodamo kakšno statistiko (št. portfeljev, transakcij, skupen vložek, donos...)
    </p>
  </div>
</div>

<div class="card bg-secondary mb-3">
  <div class="card-header fs-3">
    Upravljanje računa
  </div>
  <div class="card-body pt-1">
    <p class="fs-4 mb-0">Odjava</p>
    <div class="d-grid">
      <a class="btn btn-dark btn-block" href="/odjava/">Odjava</a>
    </div>
  </div>
  <div class="card-footer pt-1">
    <form action="/profil/" method="post">
      <p class="fs-4 mb-1">Spremeni geslo</p>
      <label for="spremeni_geslo">Novo geslo:</label>
      <input type="password" class="form-control" id="spremeni_geslo" name="spremeni_geslo" placeholder="Vnesi novo geslo" minlength="5" maxlength="20" autocomplete="new-password">
      <label for="staro_geslo">Potrdi s starim geslom:</label>
      <input type="password" class="form-control mb-1" id="staro_geslo" name="staro_geslo" placeholder="Vnesi staro geslo" minlength="5" maxlength="20">
      % if napaka:
      <div class="alert alert-danger py-1 my-1 fs-6">{{napaka}}</div>
      %end
      <div class="d-grid">
        <button class="btn btn-dark mt-2" type="submit">Potrdi spremembe</button>
      </div>
    </form>
  </div>
</div>
