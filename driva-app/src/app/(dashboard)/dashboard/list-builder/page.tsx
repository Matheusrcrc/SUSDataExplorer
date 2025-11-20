"use client";

import { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Plus, Filter, Download, Sparkles, Upload } from "lucide-react";

const mockLeads = [
  {
    id: "1",
    companyName: "Tech Solutions Ltda",
    cnpj: "12.345.678/0001-00",
    sector: "Tecnologia",
    employees: 150,
    revenue: 5000000,
    city: "São Paulo",
    state: "SP",
    email: "contato@techsolutions.com.br",
    phone: "(11) 98765-4321",
    enriched: true,
    status: "NEW",
  },
  {
    id: "2",
    companyName: "Inovação Digital S.A.",
    cnpj: "23.456.789/0001-00",
    sector: "Software",
    employees: 80,
    revenue: 3000000,
    city: "Rio de Janeiro",
    state: "RJ",
    email: "info@inovacaodigital.com",
    phone: "(21) 97654-3210",
    enriched: false,
    status: "CONTACTED",
  },
];

export default function ListBuilderPage() {
  const [showFilters, setShowFilters] = useState(false);
  const [selectedLeads, setSelectedLeads] = useState<string[]>([]);

  const handleEnrich = () => {
    console.log("Enriquecendo leads:", selectedLeads);
  };

  const handleExport = () => {
    console.log("Exportando leads");
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">List Builder</h1>
          <p className="text-muted-foreground">
            Filtre, enriqueça e gerencie seus leads
          </p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" onClick={() => document.getElementById("leads-upload")?.click()}>
            <Upload className="h-4 w-4 mr-2" />
            Importar Lista
          </Button>
          <input
            id="leads-upload"
            type="file"
            accept=".csv,.xlsx,.xls"
            className="hidden"
          />
          <Button variant="outline" onClick={() => setShowFilters(!showFilters)}>
            <Filter className="h-4 w-4 mr-2" />
            Filtros
          </Button>
          <Button>
            <Plus className="h-4 w-4 mr-2" />
            Novo Lead
          </Button>
        </div>
      </div>

      {/* Filtros */}
      {showFilters && (
        <Card>
          <CardHeader>
            <CardTitle>Filtros Avançados</CardTitle>
            <CardDescription>
              Refine sua lista de leads com critérios específicos
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid gap-4 md:grid-cols-4">
              <div className="space-y-2">
                <Label htmlFor="filter-sector">Setor</Label>
                <Input id="filter-sector" placeholder="Ex: Tecnologia" />
              </div>
              <div className="space-y-2">
                <Label htmlFor="filter-state">Estado</Label>
                <Input id="filter-state" placeholder="Ex: SP" />
              </div>
              <div className="space-y-2">
                <Label htmlFor="filter-employees">Funcionários</Label>
                <Input id="filter-employees" type="number" placeholder="Mínimo" />
              </div>
              <div className="space-y-2">
                <Label htmlFor="filter-revenue">Faturamento</Label>
                <Input id="filter-revenue" type="number" placeholder="Mínimo" />
              </div>
            </div>
            <div className="mt-4">
              <Button>Aplicar Filtros</Button>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Ações em Massa */}
      {selectedLeads.length > 0 && (
        <Card className="bg-primary/5 border-primary/20">
          <CardContent className="py-4">
            <div className="flex items-center justify-between">
              <p className="text-sm font-medium">
                {selectedLeads.length} lead(s) selecionado(s)
              </p>
              <div className="flex gap-2">
                <Button size="sm" variant="outline" onClick={handleEnrich}>
                  <Sparkles className="h-4 w-4 mr-2" />
                  Enriquecer Dados
                </Button>
                <Button size="sm" variant="outline" onClick={handleExport}>
                  <Download className="h-4 w-4 mr-2" />
                  Exportar Selecionados
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Tabela de Leads */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle>Lista de Leads</CardTitle>
              <CardDescription>
                {mockLeads.length} leads encontrados
              </CardDescription>
            </div>
            <Button variant="outline" onClick={handleExport}>
              <Download className="h-4 w-4 mr-2" />
              Exportar Todos
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b">
                  <th className="text-left py-3 px-4">
                    <input
                      type="checkbox"
                      onChange={(e) => {
                        if (e.target.checked) {
                          setSelectedLeads(mockLeads.map((l) => l.id));
                        } else {
                          setSelectedLeads([]);
                        }
                      }}
                    />
                  </th>
                  <th className="text-left py-3 px-4">Empresa</th>
                  <th className="text-left py-3 px-4">CNPJ</th>
                  <th className="text-left py-3 px-4">Setor</th>
                  <th className="text-left py-3 px-4">Localização</th>
                  <th className="text-left py-3 px-4">Funcionários</th>
                  <th className="text-left py-3 px-4">Faturamento</th>
                  <th className="text-left py-3 px-4">Contato</th>
                  <th className="text-left py-3 px-4">Status</th>
                  <th className="text-left py-3 px-4">Ações</th>
                </tr>
              </thead>
              <tbody>
                {mockLeads.map((lead) => (
                  <tr key={lead.id} className="border-b hover:bg-muted/50">
                    <td className="py-3 px-4">
                      <input
                        type="checkbox"
                        checked={selectedLeads.includes(lead.id)}
                        onChange={(e) => {
                          if (e.target.checked) {
                            setSelectedLeads([...selectedLeads, lead.id]);
                          } else {
                            setSelectedLeads(selectedLeads.filter((id) => id !== lead.id));
                          }
                        }}
                      />
                    </td>
                    <td className="py-3 px-4">
                      <div>
                        <p className="font-medium">{lead.companyName}</p>
                        {lead.enriched && (
                          <span className="text-xs text-green-600 flex items-center gap-1">
                            <Sparkles className="h-3 w-3" />
                            Enriquecido
                          </span>
                        )}
                      </div>
                    </td>
                    <td className="py-3 px-4 text-sm">{lead.cnpj}</td>
                    <td className="py-3 px-4 text-sm">{lead.sector}</td>
                    <td className="py-3 px-4 text-sm">{`${lead.city}, ${lead.state}`}</td>
                    <td className="py-3 px-4 text-sm">{lead.employees}</td>
                    <td className="py-3 px-4 text-sm">
                      R$ {(lead.revenue / 1000000).toFixed(1)}M
                    </td>
                    <td className="py-3 px-4 text-sm">
                      <div>
                        <p className="text-xs">{lead.email}</p>
                        <p className="text-xs text-muted-foreground">{lead.phone}</p>
                      </div>
                    </td>
                    <td className="py-3 px-4">
                      <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                        {lead.status}
                      </span>
                    </td>
                    <td className="py-3 px-4">
                      <Button size="sm" variant="outline">
                        Ver Detalhes
                      </Button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
