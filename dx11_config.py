IA_stage_func = set({'IASetIndexBuffer','IASetVertexBuffers','IASetInputLayout',})
VS_stage_func = set({'VSSetShader','VSSetConstantBuffers','VSSetShaderResources',})
HS_stage_func = set({'HSSetShader','HSSetConstantBuffers','HSSetShaderResources','HSSetSamplers'})
TS_stage_func = set({'TSSetShader','TSSetConstantBuffers','TSSetShaderResources',})
DS_stage_func = set({'DSSetShader','DSSetConstantBuffers','DSSetShaderResources','DSSetSamplers',})
GS_stage_func = set({'GSSetShader','GSSetConstantBuffers','GSSetShaderResources','GSSetSamplers',})
RS_stage_func = set({'RSSetState','RSSetViewports',})
PS_stage_func = set({'PSSetShader','PSSetConstantBuffers','PSSetShaderResources','PSSetSamplers',})
OM_stage_func = set({'OMSetDepthStencilState','OMSetRenderTargets','OMSetBlendState','OMSetRenderTargetsAndUnorderedAccessViews',
                'ClearDepthStencilView','ClearRenderTargetView','CopyStructureCount', 'DiscardView','DiscardResource',
                'ClearState','ClearUnorderedAccessViewFloat',
                })
CS_stage_func = set({'CSSetShader','CSSetConstantBuffers','CSSetShaderResources','CSSetSamplers','CSSetUnorderedAccessViews',})

#draw_stage_func = set({"Dispatch"})
draw_stage_func = set({'Draw','DrawIndexedInstanced','DrawIndexed','DrawAuto',
                        'Dispatch','DispatchIndirect','DrawIndexedInstancedIndirect','DrawInstanced','DrawInstancedIndirect',})

draw_stage_func1 = set({'Draw','DrawIndexedInstanced','DrawIndexed','DrawAuto',
                        'DispatchIndirect','DrawIndexedInstancedIndirect','DrawInstanced','DrawInstancedIndirect',})

dx11_device_func = set({'CreateSwapChain','CreateRenderTargetView','CreateGeometryShader','CreateQuery',
               'CreateUnorderedAccessView','CreateInputLayout','CreateDepthStencilView',
               'CreateVertexShader','CreatePixelShader','CreateShaderResourceView','CreateTexture3D',
               'CreateSamplerState','CreateDepthStencilState','CreateBlendState', 
               'CreateTexture2D','CreateComputeShader','CreateRasterizerState','CreateBuffer','CreateHullShader','CreateDomainShader',
                'CreateDeferredContext','CreateGeometryShaderWithStreamOutput','CreatePredicate',
                'CreateTexture1D','CreateBlendState1','CreateDeferredContext1',
                'CreateDeviceContextState','CreateQuery1','CreateRenderTargetView1',
                'CreateShaderResourceView1','CreateTexture2D1','CreateTexture3D1',
                'CreateUnorderedAccessView1','CreateFence',"CreateRasterizerState1",
                "CreateDXGIFactory1","CreateSwapChain",
                'CopyResource','CopyCounter','CopyTiles','CopyTileMappings','CopyBufferRegion','CopySubresourceRegion',"GetBuffer",


                 
                })


obj_set_func = IA_stage_func | VS_stage_func | HS_stage_func | TS_stage_func | DS_stage_func | GS_stage_func | RS_stage_func | PS_stage_func | OM_stage_func | CS_stage_func | draw_stage_func

map_func = set({'Map','Unmap','axdUpdatePtrFromFileInCtx11'})


# 一定添加的，不管是不是资源
must_add = set({'axdRelease','GetBuffer','IASetPrimitiveTopology','GenerateMips','D3DCompileFromFile','CreateDXGIFactory1'
                'CopyResource','CopyStructureCount','CopyCounter','CopyTiles','CopyTileMappings','CopyBufferRegion','CopySubresourceRegion',
                "CreateDXGIFactory1","D3D11CreateDevice","CreateSwapChain","axCreateWindow","D3D11CreateDevice",})

# IASetPrimitiveTopology 保证在一个Draw添加一次即可# get Buffer 一次
# 为了生成一个inject文件
copy_func = set()
#copy_func = set({'CopyResource','CopyStructureCount','CopyCounter','CopyTiles','CopyTileMappings','CopyBufferRegion','CopySubresourceRegion',})




other_func = set({'Flush','ClearState','Present','CreateDXGIFactory1'})