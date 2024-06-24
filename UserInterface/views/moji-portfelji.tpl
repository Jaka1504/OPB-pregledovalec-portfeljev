% rebase("base.tpl", title="Moji portfelji")


<h1>Moji portfelji</h1>
<div class="card bg-secondary">
  % if portfelji:
  <div class="card-header">
    <p class="mb-0">
      Kliknite na gumb na desni za podrobnejši vpogled ali urejanje posameznega portfelja.
    </p>
  </div>
  <div class="card-body py-0">
    <div class="tabela-scroll d-grid">
      <table class="table text-light">
        <thead class="fixed-head bg-secondary">
          <tr>
            <th scope="col" class="fixed-head">Ime</th>
            <th scope="col" class="fixed-head text-end">Začetni vložek</th>
            <th scope="col" class="fixed-head text-end">Vrednost</th>
            <th scope="col" class="fixed-head text-end">Donos</th>
            <th scope="col" class="fixed-head text-end">Trend 24h</th>
            <th scope="col" class="fixed-head text-end">Trend 7d</th>
            <th scope="col" class="fixed-head text-end">Vpogled</th>
          </tr>
        </thead>
        <tbody>
          % for portfelj in portfelji:
          <tr>
            <th scope="row">
              {{portfelj.ime}}
            </th>
            <td class="text-end">
              {{f"{portfelj.vlozek:.2f}"}} $
            </td>
            <td class="text-end">
              {{f"{portfelj.vrednost:.2f}"}} $
            </td>
            <td class="text-end">
              {{f"{portfelj.vrednost - portfelj.vlozek:.2f}"}} $
            </td>
            <td class="text-end">
              % if portfelj.trend24h >= 0: 
              <span class="besedilo-zeleno">{{f"{portfelj.trend24h:.2f}"}} % ▲</span>
              % else:
              <span class="besedilo-rdece">{{f"{portfelj.trend24h:.2f}"}} % ▼</span>
              % end
            </td>
            <td class="text-end">
              % if portfelj.trend7d >= 0: 
              <span class="besedilo-zeleno">{{f"{portfelj.trend7d:.2f}"}} % ▲</span>
              % else:
              <span class="besedilo-rdece">{{f"{portfelj.trend7d:.2f}"}} % ▼</span>
              % end
            </td>
            <td class="text-end text-light">
              <a class="btn btn-outline-light m-0 px-3 py-0" href="/portfelj/{{portfelj.id}}/">
                <img src="/img/search.svg" class="invert"></img>
              </a>
            </td>
          </tr>
          % end
        </tbody>
        <tfoot class="fixed-foot bg-secondary">
          <tr>
            <th scope="row" class="fixed-foot">
              SKUPAJ
            </th>
            <td class="fixed-foot text-end">
              % skupen_vlozek = sum([portfelj.vlozek for portfelj in portfelji])
              {{f"{skupen_vlozek:.2f}"}} $
            </td>
            <td class="fixed-foot text-end">
              % skupna_vrednost = sum([portfelj.vrednost for portfelj in portfelji])
              {{f"{skupna_vrednost:.2f}"}} $
            </td>
            <td class="fixed-foot text-end">
              {{f"{skupna_vrednost - skupen_vlozek:.2f}"}} $
            </td>
            <td class="fixed-foot text-end">
              % skupen_trend24h = sum([portfelj.trend24h * portfelj.vrednost for portfelj in portfelji]) / skupna_vrednost if skupna_vrednost else 0
              % if skupen_trend24h >= 0: 
              <span class="besedilo-zeleno">{{f"{skupen_trend24h:.2f}"}} % ▲</span>
              % else:
              <span class="besedilo-rdece">{{f"{skupen_trend24h:.2f}"}} % ▼</span>
              % end
            </td>
            <td class="fixed-foot text-end">
              % skupen_trend7d = sum([portfelj.trend7d * portfelj.vrednost for portfelj in portfelji]) / skupna_vrednost if skupna_vrednost else 0
              % if skupen_trend7d >= 0: 
              <span class="besedilo-zeleno">{{f"{skupen_trend7d:.2f}"}} % ▲</span>
              % else:
              <span class="besedilo-rdece">{{f"{skupen_trend7d:.2f}"}} % ▼</span>
              % end
            </td>
            <td class="fixed-foot">
            </td>
          </tr>
        </tfoot>
      </table>
    </div>
    <div class="row mb-3" width="100%">
      <div class="col d-grid">
        <a class="btn btn-dark btn-block" href="/dodaj-denar/">Dodaj denar na portfelj</a>
      </div>
      <div class="col d-grid">
        <a class="btn btn-dark btn-block" href="/nov-portfelj/">Dodaj nov portfelj</a>
      </div>
    </div>
  </div>
  % else:
  <div class="card-body">
    <p class="mb-1">
      Trenutno nimate na tem računu še nobenega portfelja. Ustvarite svoj prvi portfelj s klikom na spodnji gumb.
    </p>
    <div class="row mb-0" width="100%">
      <div class="col d-grid">
        <a class="btn btn-dark btn-block" href="/nov-portfelj/">Dodaj nov portfelj</a>
      </div>
    </div>
  </div>
  % end
</div>