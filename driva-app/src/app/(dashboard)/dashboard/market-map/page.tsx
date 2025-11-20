"use client";

import { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Map, Filter, Download } from "lucide-react";

export default function MarketMapPage() {
  const [filters, setFilters] = useState({
    sector: "",
    state: "",
    minRevenue: "",
    maxRevenue: "",
  });

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">
            Mapeamento de Mercado
          </h1>
          <p className="text-muted-foreground">
            Visualize o potencial de mercado por região e setor
          </p>
        </div>
        <Button>
          <Download className="h-4 w-4 mr-2" />
          Exportar Dados
        </Button>
      </div>

      <div className="grid gap-6 lg:grid-cols-4">
        {/* Filtros */}
        <Card className="lg:col-span-1">
          <CardHeader>
            <CardTitle className="text-base flex items-center gap-2">
              <Filter className="h-4 w-4" />
              Filtros
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="sector">Setor</Label>
              <Input
                id="sector"
                placeholder="Ex: Tecnologia"
                value={filters.sector}
                onChange={(e) => setFilters({ ...filters, sector: e.target.value })}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="state">Estado</Label>
              <Input
                id="state"
                placeholder="Ex: SP"
                value={filters.state}
                onChange={(e) => setFilters({ ...filters, state: e.target.value })}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="minRevenue">Faturamento Mín (R$)</Label>
              <Input
                id="minRevenue"
                type="number"
                placeholder="1000000"
                value={filters.minRevenue}
                onChange={(e) => setFilters({ ...filters, minRevenue: e.target.value })}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="maxRevenue">Faturamento Máx (R$)</Label>
              <Input
                id="maxRevenue"
                type="number"
                placeholder="10000000"
                value={filters.maxRevenue}
                onChange={(e) => setFilters({ ...filters, maxRevenue: e.target.value })}
              />
            </div>
            <Button className="w-full">Aplicar Filtros</Button>
          </CardContent>
        </Card>

        {/* Mapa */}
        <Card className="lg:col-span-3">
          <CardHeader>
            <CardTitle>Heatmap de Oportunidades</CardTitle>
            <CardDescription>
              Visualização geográfica do potencial de mercado
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-[500px] flex items-center justify-center border-2 border-dashed rounded-lg bg-muted/20">
              <div className="text-center">
                <Map className="h-12 w-12 mx-auto mb-4 text-muted-foreground" />
                <p className="text-lg font-medium text-muted-foreground">
                  Mapa Interativo
                </p>
                <p className="text-sm text-muted-foreground mt-2">
                  Integração com Leaflet/Mapbox será implementada aqui
                </p>
                <p className="text-xs text-muted-foreground mt-2">
                  Exibirá densidade de empresas, faturamento médio e oportunidades por região
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Estatísticas por Região */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader>
            <CardTitle className="text-sm font-medium">São Paulo</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">15,234</div>
            <p className="text-xs text-muted-foreground">Empresas</p>
            <div className="mt-2">
              <p className="text-sm font-medium">R$ 2.5B</p>
              <p className="text-xs text-muted-foreground">Faturamento Total</p>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-sm font-medium">Rio de Janeiro</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">8,456</div>
            <p className="text-xs text-muted-foreground">Empresas</p>
            <div className="mt-2">
              <p className="text-sm font-medium">R$ 1.2B</p>
              <p className="text-xs text-muted-foreground">Faturamento Total</p>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-sm font-medium">Minas Gerais</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">6,789</div>
            <p className="text-xs text-muted-foreground">Empresas</p>
            <div className="mt-2">
              <p className="text-sm font-medium">R$ 890M</p>
              <p className="text-xs text-muted-foreground">Faturamento Total</p>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-sm font-medium">Outros Estados</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">12,345</div>
            <p className="text-xs text-muted-foreground">Empresas</p>
            <div className="mt-2">
              <p className="text-sm font-medium">R$ 1.8B</p>
              <p className="text-xs text-muted-foreground">Faturamento Total</p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
