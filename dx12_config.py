

dx12_device_func = set({

    "CreateComputePipelineState","CreateGraphicsPipelineState","CreateSwapChainForHwnd","CreateFence", "GetBuffer",
    "CreateHeap","CreateCommandList",
    
    "CreateDescriptorHeap","CreateCommandSignature","CreatePlacedResource","CreateRootSignature",
    "CreateCommandQueue",            
})

dx12_device_func2 = set({
                        
                         })


pCmdList = set({"SetGraphicsRootConstantBufferView",
                "SetPipelineState","SetGraphicsRootDescriptorTable","SetDescriptorHeaps","SetGraphicsRootSignature","SetComputeRoot32BitConstants",
                "SetComputeRootDescriptorTable",  "SetComputeRootConstantBufferView","SetComputeRootSignature","SetGraphicsRoot32BitConstants",
                "IASetIndexBuffer","IASetPrimitiveTopology","IASetVertexBuffers",
                "RSSetScissorRects", "RSSetViewports","OMSetRenderTargets",
                "Close","Reset",
                "DrawIndexedInstanced","DrawInstanced","Dispatch",
                "ResourceBarrier",
                "ClearRenderTargetView","ClearDepthStencilView","ClearUnorderedAccessViewFloat","ExecuteIndirect",
                "ClearUnorderedAccessViewUint","DiscardResource",
                "CopyTextureRegion","CopyBufferRegion","CopyResource",
                
                })
must_add_func_12 = set({"ResizeBuffers1", 
                     "SetEventOnCompletion","Signal","Wait","OMSetRenderTargets",
                     "Reset","Present","RSSetViewports",
                     "CopyBufferRegion","CopyTextureRegion","CopyResource", # 提升正确值
                     "CreateCommittedResource",
                     "CreateCommandAllocator", 
                     "CreateRenderTargetView", 
                     "CreateDepthStencilView",
                    "CreateShaderResourceView",
                    "CreateUnorderedAccessView", # 1M
                     "CreateSampler", # 会影响最后正确值
                     "CreateConstantBufferView",# 会影响最后正确值

                     })
pCmdList_set_func = set({"SetDescriptorHeaps","Close","ExecuteCommandLists"})

fence_obj_func = set({"SetEventOnCompletion","Signal","Wait","GetCompletedValue"})

cmdQueue_obj_func = set({"ExecuteCommandLists","Signal","Wait",})

cmdAlloc_obj_func = set({"Reset"})

commitRes_obj_func = set({"Map","Unmap"})

swap_obj_func = set({"Present","GetBuffer","ResizeBuffers1"})

# Fac_obj_func = set({"CreateSwapChainForHwnd",})

object_func = pCmdList | fence_obj_func | cmdQueue_obj_func | cmdAlloc_obj_func | commitRes_obj_func | swap_obj_func 


func_set = set({"axdHintResourceSize","D3D12SerializeRootSignature","axdRelease","D3D11CreateDevice",
                "axdHintResourceGpuVirtualAddr","CreateDXGIFactory1","D3D12CreateDevice","axMemCpy",
                "D3DCompileFromFile","axPath"})


texture_type = set({"D3D12_RESOURCE_DIMENSION_TEXTURE2D","D3D12_RESOURCE_DIMENSION_TEXTURE1D","D3D12_RESOURCE_DIMENSION_TEXTURE3D"})














