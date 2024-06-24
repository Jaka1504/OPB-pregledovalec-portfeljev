% rebase("base.tpl", title="Nova transakcija")

<h1>Dodaj novo transakcijo</h1>
<div class="card bg-secondary">
  <div class="card-body">
    <form action="/nova-transakcija/" method="post">
      <div class="form-group">
        <label for="portfelj">Portfelj:</label>
        <div class="d-grid">
          <select class="selectpicker" id="portfelj" name="portfelj" data-live-search="true" data-width="fit" data-title="Izberi portfelj..." required>
            % for portfelj in portfelji:
            <option data-tokens="{{portfelj.id}} {{portfelj.ime}}" value="{{portfelj.id}}">{{portfelj.ime}} [Stanje: {{portfelj.gotovina}} $]</option>
            % end
          </select>
        </div>
        <label for="kriptovaluta">Kriptovaluta:</label>
        <div class="d-grid">
          <select class="selectpicker" id="kriptovaluta" name="kriptovaluta" data-live-search="true" data-width="fit" data-size="15" data-noneSelectedText="Izberi kriptovaluto..." data-title="Izberi kriptovaluto..." required>
            % for kriptovaluta in vse_kriptovalute:
            <option data-tokens="{{kriptovaluta.kratica}} {{kriptovaluta.ime}}" value="{{kriptovaluta.id}}">{{kriptovaluta.ime}}, {{kriptovaluta.kratica}} [{{kriptovaluta.zadnja_cena}} $]</option>
            % end
          </select>
        </div>
        <label for="kolicina">Količina (za nakup vnesi pozitivno, za prodajo pa negativno število)</label>
        <input type="number" class="form-control" id="kolicina" name="kolicina" placeholder="Količina" step="0.000001">
      </div>
      % if napaka:
      <div class="alert alert-danger py-1 m-0 fs-6">{{napaka}}</div>
      %end
      <div class="d-grid">
        <button class="btn btn-dark mb-3 mt-1" type="submit">Potrdi nakup / prodajo</button>
      </div>
    </form>
    <label for="moji-portfelji">Nazaj na pogled trenutnih portfeljev:</label>
    <div class="d-grid">
      <a class="btn btn-dark" href="/moji-portfelji/" id="moji-portfelji">Moji portfelji</a>
    </div>
  </div>
</div>