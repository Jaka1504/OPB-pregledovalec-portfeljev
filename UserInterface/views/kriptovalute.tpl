% rebase("base.tpl", title="Kriptovaluta " + kriptovaluta["ime"])

<h2>Išči druge kriptovalute</h2>
<div class="card bg-secondary">
  <div class="card-body">
    <form action="/najdi-kripto/" method="post">
      <div class="form-group">
        <label for="kriptovaluta">Kriptovaluta:</label>
        <div class="d-grid">
          <select class="selectpicker" id="kriptovaluta" name="kriptovaluta" data-live-search="true" data-width="fit" data-size="15" data-noneSelectedText="Izberi kriptovaluto..." data-title="Izberi kriptovaluto..." required>
            % for kripto in vse_kriptovalute:
            <option data-tokens="{{kripto.kratica}} {{kripto.ime}}" value="{{kripto.id}}">{{kripto.ime}}, {{kripto.kratica}} [{{kripto.zadnja_cena}} $]</option>
            % end
          </select>
        </div>
      </div>
      <div class="d-grid">
        <button class="btn btn-dark mb-3 mt-1" type="submit">Pojdi</button>
      </div>
    </form>
  </div>
</div>

<h2>Kriptovaluta {{kriptovaluta["ime"]}}</h2>
<div class="card bg-secondary mb-6">
  <div class="card-header">
    <h3>Podrobnosti</h3>
  </div>
  <div class="card-body py-0">
    <div class="container">
      <div class="row">
        <div class="col">
          <table class="table text-light">
            <tbody>
              <tr><td class="py-0">Ime</td><td class="py-0 text-end">{{kriptovaluta["ime"]}}</td></tr>
              <tr><td class="py-0">Kratica</td><td class="py-0 text-end">{{kriptovaluta["kratica"]}}</td></tr>
              <tr><td class="py-0">Vrednost ene enote</td><td class="py-0 text-end">{{f"{kriptovaluta['vrednost_enote']:.4f}"}} $</td></tr>
              <tr>
                <td class="py-0">Trend 24h</td>
                <td class="py-0 text-end">
                  % if kriptovaluta["trend24h"] >= 0: 
                  <span class="besedilo-zeleno">{{f"{kriptovaluta['trend24h']:.2f}"}} % ▲</span>
                  % else:
                  <span class="besedilo-rdece">{{f"{kriptovaluta['trend24h']:.2f}"}} % ▼</span>
                  % end
                </td>
              </tr>
              <tr>
                <td class="py-0">Trend 7d</td>
                <td class="py-0 text-end">
                  % if kriptovaluta["trend7d"] >= 0: 
                  <span class="besedilo-zeleno">{{f"{kriptovaluta['trend7d']:.2f}"}} % ▲</span>
                  % else:
                  <span class="besedilo-rdece">{{f"{kriptovaluta['trend7d']:.2f}"}} % ▼</span>
                  % end
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="col">
          {{!graf}}
        </div>
      </div>
    </div>
    <div class="row mb-3" width=100%"> 
      <div class="col d-grid">
        <a class="btn btn-dark btn-block" href="/nova-transakcija/">Dodaj transakcijo</a>
      </div>
    </div>
  </div>
</div>

<div class="container-fluid text-dark">   <!-- To je precej cigansko, probej popravit -->
  .
</div>
