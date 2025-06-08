"use client"

import { useState } from "react"
import { ChevronRight, ChevronDown, Home, ArrowLeft } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from "@/components/ui/collapsible"
import { Separator } from "@/components/ui/separator"

interface NavigationState {
  tp?: number
  punto?: number
  inciso?: string
}

interface ContentData {
  title: string
  description: string
  graphData?: any
  results?: string[]
}

export default function AnalisisNumerico() {
  const [navigation, setNavigation] = useState<NavigationState>({})
  const [openTPs, setOpenTPs] = useState<number[]>([])
  const [openPuntos, setOpenPuntos] = useState<string[]>([])
  const [contentData, setContentData] = useState<ContentData | null>(null)
  const [loading, setLoading] = useState(false)

  const toggleTP = (tpNumber: number) => {
    setOpenTPs((prev) => (prev.includes(tpNumber) ? prev.filter((tp) => tp !== tpNumber) : [...prev, tpNumber]))
  }

  const togglePunto = (tpNumber: number, puntoNumber: number) => {
    const key = `${tpNumber}-${puntoNumber}`
    setOpenPuntos((prev) => (prev.includes(key) ? prev.filter((p) => p !== key) : [...prev, key]))
  }

  const selectInciso = async (tp: number, punto: number, inciso: string) => {
    setNavigation({ tp, punto, inciso })
    setLoading(true)

    // Simular llamada al backend Python
    setTimeout(() => {
      setContentData({
        title: `TP${tp} - Punto ${punto} - Inciso ${inciso}`,
        description: `Análisis matemático para el Trabajo Práctico ${tp}, Punto ${punto}, Inciso ${inciso}`,
        results: [
          "Matriz de entrada procesada correctamente",
          "Transformada de Fourier 2D aplicada",
          "Eigenvalores calculados: λ₁ = 2.45, λ₂ = -1.33, λ₃ = 0.87",
          "Convergencia alcanzada en 15 iteraciones",
          "Error relativo: 1.2e-6",
        ],
      })
      setLoading(false)
    }, 1000)
  }

  const goBack = () => {
    if (navigation.inciso) {
      setNavigation({ tp: navigation.tp, punto: navigation.punto })
      setContentData(null)
    } else if (navigation.punto) {
      setNavigation({ tp: navigation.tp })
    } else if (navigation.tp) {
      setNavigation({})
    }
  }

  const goHome = () => {
    setNavigation({})
    setContentData(null)
  }

  const getBreadcrumbs = () => {
    const breadcrumbs = []
    if (navigation.tp) {
      breadcrumbs.push(`TP${navigation.tp}`)
    }
    if (navigation.punto) {
      breadcrumbs.push(`Punto ${navigation.punto}`)
    }
    if (navigation.inciso) {
      breadcrumbs.push(`Inciso ${navigation.inciso}`)
    }
    return breadcrumbs
  }

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Sidebar */}
      <div className="w-80 bg-white border-r border-gray-200 overflow-y-auto">
        <div className="p-6">
          <h1 className="text-2xl font-bold text-gray-900 mb-6">Análisis Numérico 2025</h1>

          <nav className="space-y-2">
            {[1, 2, 3, 4, 5, 6].map((tpNumber) => (
              <Collapsible key={tpNumber} open={openTPs.includes(tpNumber)}>
                <CollapsibleTrigger asChild>
                  <Button
                    variant="ghost"
                    className="w-full justify-between p-3 h-auto"
                    onClick={() => toggleTP(tpNumber)}
                  >
                    <span className="font-medium">Trabajo Práctico N°{tpNumber}</span>
                    {openTPs.includes(tpNumber) ? (
                      <ChevronDown className="h-4 w-4" />
                    ) : (
                      <ChevronRight className="h-4 w-4" />
                    )}
                  </Button>
                </CollapsibleTrigger>
                <CollapsibleContent className="ml-4 space-y-1">
                  {[1, 2, 3].map((puntoNumber) => (
                    <Collapsible key={puntoNumber} open={openPuntos.includes(`${tpNumber}-${puntoNumber}`)}>
                      <CollapsibleTrigger asChild>
                        <Button
                          variant="ghost"
                          className="w-full justify-between p-2 h-auto text-sm"
                          onClick={() => togglePunto(tpNumber, puntoNumber)}
                        >
                          <span>Punto {puntoNumber}</span>
                          {openPuntos.includes(`${tpNumber}-${puntoNumber}`) ? (
                            <ChevronDown className="h-3 w-3" />
                          ) : (
                            <ChevronRight className="h-3 w-3" />
                          )}
                        </Button>
                      </CollapsibleTrigger>
                      <CollapsibleContent className="ml-4 space-y-1">
                        {["a", "b"].map((inciso) => (
                          <Button
                            key={inciso}
                            variant="ghost"
                            className="w-full justify-start p-2 h-auto text-sm text-gray-600 hover:text-gray-900"
                            onClick={() => selectInciso(tpNumber, puntoNumber, inciso)}
                          >
                            Inciso {inciso}
                          </Button>
                        ))}
                      </CollapsibleContent>
                    </Collapsible>
                  ))}
                </CollapsibleContent>
              </Collapsible>
            ))}
          </nav>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Header with breadcrumbs */}
        <div className="bg-white border-b border-gray-200 p-4">
          <div className="flex items-center space-x-4">
            <Button variant="outline" size="sm" onClick={goHome}>
              <Home className="h-4 w-4 mr-2" />
              Inicio
            </Button>
            {navigation.tp && (
              <Button variant="outline" size="sm" onClick={goBack}>
                <ArrowLeft className="h-4 w-4 mr-2" />
                Volver
              </Button>
            )}
            {getBreadcrumbs().length > 0 && (
              <div className="flex items-center space-x-2 text-sm text-gray-600">
                <span>Navegación:</span>
                {getBreadcrumbs().map((crumb, index) => (
                  <span key={index} className="flex items-center">
                    {index > 0 && <ChevronRight className="h-3 w-3 mx-1" />}
                    <span className="font-medium">{crumb}</span>
                  </span>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Content Area */}
        <div className="flex-1 p-6 overflow-y-auto">
          {!navigation.inciso ? (
            <div className="flex items-center justify-center h-full">
              <Card className="w-full max-w-2xl">
                <CardHeader>
                  <CardTitle className="text-center">Bienvenido a Análisis Numérico 2025</CardTitle>
                </CardHeader>
                <CardContent className="text-center text-gray-600">
                  <p className="mb-4">Selecciona un trabajo práctico, punto e inciso del menú lateral para comenzar.</p>
                  <p className="text-sm">
                    Este sistema te permitirá visualizar gráficas y resultados de cálculos matemáticos incluyendo
                    análisis de matrices, transformadas de Fourier 2D, búsqueda de raíces y resolución de ecuaciones
                    diferenciales.
                  </p>
                </CardContent>
              </Card>
            </div>
          ) : (
            <div className="space-y-6">
              {/* Title */}
              <div>
                <h2 className="text-3xl font-bold text-gray-900 mb-2">{contentData?.title}</h2>
                <p className="text-gray-600">{contentData?.description}</p>
              </div>

              <Separator />

              {loading ? (
                <div className="flex items-center justify-center py-12">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                  <span className="ml-3 text-gray-600">Cargando datos del backend...</span>
                </div>
              ) : (
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  {/* Graph Area */}
                  <Card>
                    <CardHeader>
                      <CardTitle>Visualización Gráfica</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="aspect-square bg-gray-100 rounded-lg flex items-center justify-center">
                        <div className="text-center text-gray-500">
                          <div className="w-16 h-16 mx-auto mb-4 bg-blue-100 rounded-lg flex items-center justify-center">
                            📊
                          </div>
                          <p className="font-medium">Gráfica generada</p>
                          <p className="text-sm">Datos del backend Python</p>
                        </div>
                      </div>
                    </CardContent>
                  </Card>

                  {/* Results Area */}
                  <Card>
                    <CardHeader>
                      <CardTitle>Resultados del Análisis</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-3">
                        {contentData?.results?.map((result, index) => (
                          <div key={index} className="p-3 bg-gray-50 rounded-lg">
                            <p className="text-sm font-mono">{result}</p>
                          </div>
                        ))}
                      </div>
                    </CardContent>
                  </Card>
                </div>
              )}

              {/* Additional Analysis Section */}
              <Card>
                <CardHeader>
                  <CardTitle>Análisis Detallado</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="p-4 bg-blue-50 rounded-lg">
                      <h4 className="font-semibold text-blue-900 mb-2">Matrices</h4>
                      <p className="text-sm text-blue-700">Análisis de eigenvalores y eigenvectores</p>
                    </div>
                    <div className="p-4 bg-green-50 rounded-lg">
                      <h4 className="font-semibold text-green-900 mb-2">Fourier 2D</h4>
                      <p className="text-sm text-green-700">Transformada aplicada correctamente</p>
                    </div>
                    <div className="p-4 bg-purple-50 rounded-lg">
                      <h4 className="font-semibold text-purple-900 mb-2">Convergencia</h4>
                      <p className="text-sm text-purple-700">Método numérico convergente</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="bg-white border-t border-gray-200 p-4">
          <p className="text-center text-sm text-gray-600">
            Desarrollado por Bagnarol Audicio, Danelone, Farías, Padulli & Rafart
          </p>
        </div>
      </div>
    </div>
  )
}
