% rebase("base.tpl", title="Portfelj " + portfelj.ime)


% skupna_vrednost = sum([kriptovaluta["vrednost"] for kriptovaluta in portfelj.kriptovalute.values()])


<h1>Portfelj {{portfelj.ime}}</h1>
<div class="card bg-secondary">
  <div class="card-header">


    <div class="container">
      <div class="row">
        <div class="col">
          <table class="table text-light">
            <tbody>
              <tr><td class="py-0">Začetni vložek</td><td class="py-0 text-end">{{f"{portfelj.vlozek:.2f}"}} $</td></tr>
              <tr><td class="py-0">Denar na portfelju</td><td class="py-0 text-end">{{f"{portfelj.gotovina:.2f}"}} $</td></tr>
              <tr><td class="py-0">Skupna vrednost</td><td class="py-0 text-end">{{f"{skupna_vrednost + portfelj.gotovina:.2f}"}} $</td></tr>
              <tr><td class="py-0">Donos</td><td class="py-0 text-end">{{f"{skupna_vrednost + portfelj.gotovina - portfelj.vlozek:.2f}"}} $</td></tr>
            </tbody>
          </table>
        </div>
        <div class="col">
          {{!graf}}
        </div>
      </div>
    </div>
  </div>
  <div class="card-body py-0">
    <div class="tabela-scroll d-grid">
      <table class="table text-light">
        <thead class="fixed-head bg-secondary">
          <tr>
            <th scope="col" class="fixed-head">Kriptovaluta</th>
            <th scope="col" class="fixed-head">Kratica</th>
            <th scope="col" class="fixed-head text-end">Količina</th>
            <!-- <th scope="col" class="fixed-head text-end">Cena</th> -->
            <th scope="col" class="fixed-head text-end">Vrednost</th>
            <!-- <th scope="col" class="fixed-head text-end">Donos</th> -->
            <th scope="col" class="fixed-head text-end">Trend 24h</th>
            <th scope="col" class="fixed-head text-end">Trend 7d</th>
            <th scope="col" class="fixed-head text-end">Vpogled</th>
          </tr>
        </thead>
        <tbody>
          % for kriptovaluta in portfelj.kriptovalute.values():
          <tr>
            <th scope="row">
              {{kriptovaluta["ime"]}}
            </th>
            <td>
              {{kriptovaluta["kratica"]}}
            </td>
            <td class="text-end">
              {{f"{kriptovaluta['kolicina']:.6f}"}}
            </td>
            <td class="text-end">
              {{f"{kriptovaluta['vrednost']:.2f}"}} $
            </td>
            <td class="text-end">
              % if kriptovaluta['trend24h'] >= 0: 
              <span class="besedilo-zeleno">{{f"{kriptovaluta['trend24h']:.2f}"}} % ▲</span>
              % else:
              <span class="besedilo-rdece">{{f"{kriptovaluta['trend24h']:.2f}"}} % ▼</span>
              % end
            </td>
            <td class="text-end">
              % if kriptovaluta["trend7d"] >= 0: 
              <span class="besedilo-zeleno">{{f"{kriptovaluta['trend7d']:.2f}"}} % ▲</span>
              % else:
              <span class="besedilo-rdece">{{f"{kriptovaluta['trend7d']:.2f}"}} % ▼</span>
              % end
            </td>
            <td class="text-end text-light">
              <a class="btn btn-outline-light m-0 px-3 py-0" href="/kriptovaluta/{{portfelj.id}}/{{kriptovaluta['id']}}/">
                <img src="/img/search.svg" class="invert"></img>
              </a>
            </td>
          </tr>
          % end
        </tbody>
        <tfoot class="fixed-foot bg-secondary">
          <tr>
            <th scope="row" class="fiksna-vrstica">
              SKUPAJ
            </th>
            <td class="fixed-foot"></td> <!-- kratica -->
            <td class="fixed-foot"></td> <!-- kolicina -->
            <td class="fixed-foot text-end">
              {{f"{skupna_vrednost:.2f}"}} $
            </td>
            <td class="fixed-foot text-end">
              % skupen_trend24h = sum([kriptovaluta["trend24h"] * kriptovaluta["vrednost"] for kriptovaluta in portfelj.kriptovalute.values()]) / skupna_vrednost if skupna_vrednost else 0
              % if skupen_trend24h >= 0: 
              <span class="besedilo-zeleno">{{f"{skupen_trend24h:.2f}"}} % ▲</span>
              % else:
              <span class="besedilo-rdece">{{f"{skupen_trend24h:.2f}"}} % ▼</span>
              % end
            </td>
            <td class="fixed-foot text-end">
              % skupen_trend7d = sum([kriptovaluta["trend7d"] * kriptovaluta["vrednost"] for kriptovaluta in portfelj.kriptovalute.values()]) / skupna_vrednost  if skupna_vrednost else 0
              % if skupen_trend7d >= 0: 
              <span class="besedilo-zeleno">{{f"{skupen_trend7d:.2f}"}} % ▲</span>
              % else:
              <span class="besedilo-rdece">{{f"{skupen_trend7d:.2f}"}} % ▼</span>
              % end
            </td>
            <td class="fixed-foot"></td> <!-- vpogled -->
          </tr>
        </tfoot>
      </table>
    </div>
    <div class="row mb-3" width="100%">
      <div class="col d-grid">
        <a class="btn btn-dark btn-block" href="/dodaj-denar/">Dodaj denar na portfelj</a>
      </div>
      <div class="col d-grid">
        <a class="btn btn-dark btn-block" href="/nova-transakcija/">Dodaj novo transakcijo</a>
      </div>
    </div>
  </div>
</div>