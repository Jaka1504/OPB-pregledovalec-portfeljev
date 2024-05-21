% rebase("base.tpl", title="Moji portfelji")


<h1>Moji portfelji</h1>
<div class="card bg-secondary">
  <div class="card-header">
    <p class="mb-0">
      Kliknite na gumb na desni za podrobnejši vpogled ali urejanje posameznega portfelja.
    </p>
  </div>
  <div class="card-body py-0">
    <div class="tabela-scroll d-grid">
      <table class="table text-light">
        <thead>
          <tr>
            <th scope="col">Ime</th>
            <th scope="col" class="text-end">Cena</th>
            <th scope="col" class="text-end">Vrednost</th>
            <th scope="col" class="text-end">Donos</th>
            <th scope="col" class="text-end">Trend</th>
            <th scope="col" class="text-end">Vpogled</th>
          </tr>
        </thead>
        <tbody>
          % for portfelj in portfelji:
          <tr>
            <th scope="row">
              {{portfelj["ime"]}}
            </th>
            <td class="text-end">
              {{portfelj["cena"]}} €
            </td>
            <td class="text-end">
              {{portfelj["vrednost"]}} €
            </td>
            <td class="text-end">
              {{portfelj["donos"]}} €
            </td>
            <td class="text-end">
              % if portfelj["trend"] >= 0: 
              <span class="besedilo-zeleno">{{portfelj["trend"]}} % ▲</span>
              % else:
              <span class="besedilo-rdece">{{portfelj["trend"]}} % ▼</span>
              % end
            </td>
            <td class="text-end text-light">
              <a class="btn btn-outline-light m-0 px-3 py-0" href="/moji-portfelji/{{portfelj['id']}}">
                <img src="/img/search.svg" class="invert"></img>
              </a>
            </td>
          </tr>
          % end
          <tr>
            <th scope="row">
              SKUPAJ
            </th>
            <td class="text-end">
              {{sum([portfelj["cena"] for portfelj in portfelji])}} €
            </td>
            <td class="text-end">
              % skupna_vrednost = sum([portfelj["vrednost"] for portfelj in portfelji])
              {{skupna_vrednost}} €
            </td>
            <td class="text-end">
              {{sum([portfelj["donos"] for portfelj in portfelji])}} €
            </td>
            <td class="text-end">
              % skupen_trend = round(sum([portfelj["trend"] * portfelj["vrednost"] for portfelj in portfelji]) / skupna_vrednost, 2)
              % if skupen_trend >= 0: 
              <span class="besedilo-zeleno">{{skupen_trend}} % ▲</span>
              % else:
              <span class="besedilo-rdece">{{skupen_trend}} % ▼</span>
              % end
            </td>
            <td>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="row mb-3" width="100%">
      <div class="col d-grid">
        <a class="btn btn-dark btn-block" href="/">Posodobi stanje</a>
      </div>
      <div class="col d-grid">
        <a class="btn btn-dark btn-block" href="/">Dodaj nov portfelj</a>
      </div>
    </div>
  </div>
</div>