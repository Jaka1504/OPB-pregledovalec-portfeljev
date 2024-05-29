% rebase("base.tpl", title="Portfelj " + portfelj["ime"])


<h1>Portfelj {{portfelj["ime"]}}</h1>
<div class="card bg-secondary">
  <div class="card-header">
    <p class="mb-0">
      Kliknite na gumb na desni za podrobnejši vpogled ali urejanje posamezne kriptovalute.
    </p>
  </div>
  <div class="card-body py-0">
    <div class="tabela-scroll d-grid">
      <table class="table text-light">
        <thead class="fixed-head bg-secondary">
          <tr>
            <th scope="col" class="fixed-head">Kriptovaluta</th>
            <th scope="col" class="fixed-head">Kratica</th>
            <th scope="col" class="fixed-head text-end">Količina</th>
            <th scope="col" class="fixed-head text-end">Cena</th>
            <th scope="col" class="fixed-head text-end">Vrednost</th>
            <th scope="col" class="fixed-head text-end">Donos</th>
            <th scope="col" class="fixed-head text-end">Trend</th>
            <th scope="col" class="fixed-head text-end">Vpogled</th>
          </tr>
        </thead>
        <tbody>
          % for kriptovaluta in portfelj["kriptovalute"]:
          <tr>
            <th scope="row">
              {{kriptovaluta["ime"]}}
            </th>
            <td>
              {{kriptovaluta["kratica"]}}
            </td>
            <td class="text-end">
              {{f"{kriptovaluta["kolicina"]:.6f}"}}
            </td>
            <td class="text-end">
              {{f"{kriptovaluta["cena"]:.2f}"}} €
            </td>
            <td class="text-end">
              {{f"{kriptovaluta["vrednost"]:.2f}"}} €
            </td>
            <td class="text-end">
              {{f"{kriptovaluta["donos"]:.2f}"}} €
            </td>
            <td class="text-end">
              % if kriptovaluta["trend"] >= 0: 
              <span class="besedilo-zeleno">{{f"{kriptovaluta["trend"]:.2f}"}} % ▲</span>
              % else:
              <span class="besedilo-rdece">{{f"{kriptovaluta["trend"]:.2f}"}} % ▼</span>
              % end
            </td>
            <td class="text-end text-light">
              <a class="btn btn-outline-light m-0 px-3 py-0" href="/kriptovaluta/{{portfelj['id']}}/{{kriptovaluta['id']}}">
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
              {{f"{sum([kriptovaluta["cena"] for kriptovaluta in portfelj["kriptovalute"]]):.2f}"}} €
            </td>
            <td class="fixed-foot text-end">
              % skupna_vrednost = sum([kriptovaluta["vrednost"] for kriptovaluta in portfelj["kriptovalute"]])
              {{f"{skupna_vrednost:.2f}"}} €
            </td>
            <td class="fixed-foot text-end">
              {{f"{sum([kriptovaluta["donos"] for kriptovaluta in portfelj["kriptovalute"]]):.2f}"}} €
            </td>
            <td class="fixed-foot text-end">
              % skupen_trend = sum([kriptovaluta["trend"] * kriptovaluta["vrednost"] for kriptovaluta in portfelj["kriptovalute"]]) / skupna_vrednost
              % if skupen_trend >= 0: 
              <span class="besedilo-zeleno">{{f"{skupen_trend:.2f}"}} % ▲</span>
              % else:
              <span class="besedilo-rdece">{{f"{skupen_trend:.2f}"}} % ▼</span>
              % end
            </td>
            <td class="fixed-foot"></td> <!-- vpogled -->
          </tr>
        </tfoot>
      </table>
    </div>
    <div class="row mb-3" width="100%">
      <div class="col d-grid">
        <a class="btn btn-dark btn-block" href="/">Posodobi stanje</a>
      </div>
      <div class="col d-grid">
        <a class="btn btn-dark btn-block" href="/">Dodaj novo transakcijo</a>
      </div>
    </div>
  </div>
</div>