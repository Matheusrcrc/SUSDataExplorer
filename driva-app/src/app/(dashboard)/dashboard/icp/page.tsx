"use client";

import { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Plus, Upload, Target } from "lucide-react";

export default function ICPPage() {
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    name: "",
    description: "",
    sectors: "",
    locations: "",
    companySizeMin: "",
    companySizeMax: "",
    revenueMin: "",
    revenueMax: "",
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    // Aqui seria feita a chamada à API para salvar o ICP
    console.log("Salvando ICP:", formData);
    setShowForm(false);
    setFormData({
      name: "",
      description: "",
      sectors: "",
      locations: "",
      companySizeMin: "",
      companySizeMax: "",
      revenueMin: "",
      revenueMax: "",
    });
  };

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      // Aqui seria feito o processamento do arquivo
      console.log("Arquivo selecionado:", file.name);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">
            Perfil de Cliente Ideal (ICP)
          </h1>
          <p className="text-muted-foreground">
            Defina e gerencie seus perfis de clientes ideais
          </p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" onClick={() => document.getElementById("file-upload")?.click()}>
            <Upload className="h-4 w-4 mr-2" />
            Importar Planilha
          </Button>
          <input
            id="file-upload"
            type="file"
            accept=".csv,.xlsx,.xls"
            className="hidden"
            onChange={handleFileUpload}
          />
          <Button onClick={() => setShowForm(!showForm)}>
            <Plus className="h-4 w-4 mr-2" />
            Novo ICP
          </Button>
        </div>
      </div>

      {showForm && (
        <Card>
          <CardHeader>
            <CardTitle>Criar Novo Perfil ICP</CardTitle>
            <CardDescription>
              Defina os critérios do seu cliente ideal
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid gap-4 md:grid-cols-2">
                <div className="space-y-2">
                  <Label htmlFor="name">Nome do Perfil *</Label>
                  <Input
                    id="name"
                    placeholder="Ex: Empresas de TI"
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                    required
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="description">Descrição</Label>
                  <Input
                    id="description"
                    placeholder="Descrição do perfil"
                    value={formData.description}
                    onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  />
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="sectors">Setores (CNAEs)</Label>
                <Input
                  id="sectors"
                  placeholder="Ex: 6201-5/00, 6202-3/00 (separados por vírgula)"
                  value={formData.sectors}
                  onChange={(e) => setFormData({ ...formData, sectors: e.target.value })}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="locations">Localizações</Label>
                <Input
                  id="locations"
                  placeholder="Ex: São Paulo, Rio de Janeiro (separados por vírgula)"
                  value={formData.locations}
                  onChange={(e) => setFormData({ ...formData, locations: e.target.value })}
                />
              </div>

              <div className="grid gap-4 md:grid-cols-2">
                <div className="space-y-2">
                  <Label htmlFor="companySizeMin">Funcionários (Mínimo)</Label>
                  <Input
                    id="companySizeMin"
                    type="number"
                    placeholder="Ex: 10"
                    value={formData.companySizeMin}
                    onChange={(e) => setFormData({ ...formData, companySizeMin: e.target.value })}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="companySizeMax">Funcionários (Máximo)</Label>
                  <Input
                    id="companySizeMax"
                    type="number"
                    placeholder="Ex: 500"
                    value={formData.companySizeMax}
                    onChange={(e) => setFormData({ ...formData, companySizeMax: e.target.value })}
                  />
                </div>
              </div>

              <div className="grid gap-4 md:grid-cols-2">
                <div className="space-y-2">
                  <Label htmlFor="revenueMin">Faturamento Mínimo (R$)</Label>
                  <Input
                    id="revenueMin"
                    type="number"
                    placeholder="Ex: 1000000"
                    value={formData.revenueMin}
                    onChange={(e) => setFormData({ ...formData, revenueMin: e.target.value })}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="revenueMax">Faturamento Máximo (R$)</Label>
                  <Input
                    id="revenueMax"
                    type="number"
                    placeholder="Ex: 10000000"
                    value={formData.revenueMax}
                    onChange={(e) => setFormData({ ...formData, revenueMax: e.target.value })}
                  />
                </div>
              </div>

              <div className="flex gap-2">
                <Button type="submit">Salvar ICP</Button>
                <Button type="button" variant="outline" onClick={() => setShowForm(false)}>
                  Cancelar
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>
      )}

      {/* Lista de ICPs existentes */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {/* ICP exemplo */}
        <Card>
          <CardHeader>
            <div className="flex items-start justify-between">
              <div className="flex items-center gap-2">
                <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center">
                  <Target className="h-5 w-5 text-primary" />
                </div>
                <div>
                  <CardTitle className="text-base">Empresas de TI</CardTitle>
                  <CardDescription className="text-xs">
                    50-200 funcionários
                  </CardDescription>
                </div>
              </div>
            </div>
          </CardHeader>
          <CardContent>
            <div className="space-y-2 text-sm">
              <div>
                <span className="font-medium">Setores:</span> Tecnologia, Software
              </div>
              <div>
                <span className="font-medium">Localização:</span> SP, RJ, MG
              </div>
              <div>
                <span className="font-medium">Faturamento:</span> R$ 1M - R$ 10M
              </div>
              <div className="pt-2">
                <Button size="sm" variant="outline" className="w-full">
                  Ver Detalhes
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Placeholder para novos ICPs */}
        <Card className="border-dashed">
          <CardContent className="flex items-center justify-center h-full min-h-[200px]">
            <div className="text-center">
              <Target className="h-8 w-8 mx-auto mb-2 text-muted-foreground" />
              <p className="text-sm text-muted-foreground">
                Adicione mais perfis ICP
              </p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
