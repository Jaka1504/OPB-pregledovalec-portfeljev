% rebase("base.tpl", title="Portfelj " + portfelj["ime"])


<h1>Portfelj {{portfelj["ime"]}}</h1>
<div class="card bg-secondary">
  <div class="card-header">
    <p class="mb-0">
      Kliknite na gumb na desni za podrobnejši vpogled ali urejanje posamezne transakcije.
    </p>
  </div>
  <div class="card-body py-0">
    <div class="tabela-scroll d-grid">
      <table class="table text-light">
        <thead class="fixed-head bg-secondary">
          <tr>
            <th scope="col" class="fixed-head">Sredstvo</th>
            <th scope="col" class="fixed-head">Kratica</th>
            <th scope="col" class="fixed-head">Datum nakupa</th>
            <th scope="col" class="fixed-head text-end">Količina</th>
            <th scope="col" class="fixed-head text-end">Cena</th>
            <th scope="col" class="fixed-head text-end">Vrednost</th>
            <th scope="col" class="fixed-head text-end">Donos</th>
            <th scope="col" class="fixed-head text-end">Trend</th>
            <th scope="col" class="fixed-head text-end">Vpogled</th>
          </tr>
        </thead>
        <tbody>
          % for transakcija in portfelj["transakcije"]:
          <tr>
            <th scope="row">
              {{transakcija["sredstvo"]}}
            </th>
            <td>
              {{transakcija["kratica"]}}
            </td>
            <td>
              {{transakcija["datum"]}}
            </td>
            <td class="text-end">
              {{transakcija["kolicina"]}}
            </td>
            <td class="text-end">
              {{transakcija["cena"]}} €
            </td>
            <td class="text-end">
              {{transakcija["vrednost"]}} €
            </td>
            <td class="text-end">
              {{transakcija["donos"]}} €
            </td>
            <td class="text-end">
              % if transakcija["trend"] >= 0: 
              <span class="besedilo-zeleno">{{transakcija["trend"]}} % ▲</span>
              % else:
              <span class="besedilo-rdece">{{transakcija["trend"]}} % ▼</span>
              % end
            </td>
            <td class="text-end text-light">
              <a class="btn btn-outline-light m-0 px-3 py-0" href="/transakcija/{{transakcija['id']}}">
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
            <td class="fixed-foot"></td> <!-- datum -->
            <td class="fixed-foot"></td> <!-- kolicina -->
            <td class="fixed-foot text-end">
              {{round(sum([transakcija["cena"] for transakcija in portfelj["transakcije"]]), 2)}} €
            </td>
            <td class="fixed-foot text-end">
              % skupna_vrednost = sum([transakcija["vrednost"] for transakcija in portfelj["transakcije"]])
              {{round(skupna_vrednost, 2)}} €
            </td>
            <td class="fixed-foot text-end">
              {{round(sum([transakcija["donos"] for transakcija in portfelj["transakcije"]]), 2)}} €
            </td>
            <td class="fixed-foot text-end">
              % skupen_trend = round(sum([transakcija["trend"] * transakcija["vrednost"] for transakcija in portfelj["transakcije"]]) / skupna_vrednost, 2)
              % if skupen_trend >= 0: 
              <span class="besedilo-zeleno">{{skupen_trend}} % ▲</span>
              % else:
              <span class="besedilo-rdece">{{skupen_trend}} % ▼</span>
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