% rebase("base.tpl", title="Nov portfelj")

<h1>Ustvari nov portfelj</h1>
<div class="card bg-secondary">
  <div class="card-body">
    <form action="/nov-portfelj/" method="post">
      <div class="form-group">
        <label for="vlozek">Ime portfelja:</label>
        <input type="text" class="form-control" id="ime_portfelja" name="ime_portfelja" placeholder="Ime portfelja" minlength="2" maxlength="30">
        <label for="vlozek">Začetni vložek (USD):</label>
        <input type="number" class="form-control" id="vlozek" name="vlozek" placeholder="Začetni vložek" step="0.01" min="0">
      </div>
      % if napaka:
      <div class="alert alert-danger py-1 m-0 fs-6">{{napaka}}</div>
      %end
      <div class="d-grid">
        <button class="btn btn-dark mb-3 mt-1" type="submit">Ustvari nov portfelj</button>
      </div>
    </form>
    <label for="moji-portfelji">Nazaj na pogled trenutnih portfeljev:</label>
    <div class="d-grid">
      <a class="btn btn-dark" href="/moji-portfelji/" id="moji-portfelji">Moji portfelji</a>
    </div>
  </div>
</div>