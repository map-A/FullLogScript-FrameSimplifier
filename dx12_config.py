

dx12_device_func = set({
    "CreateCommandQueue","CreatePlacedResource","CreateRootSignature","CreateShaderResourceView",
    "CreateComputePipelineState","CreateGraphicsPipelineState","CreateCommittedResource","CreateRenderTargetView",
    "CreateCommandSignature","CreateHeap","CreateCommandList","CreateSampler",
    "CreateDepthStencilView","CreateDescriptorHeap","CreateUnorderedAccessView","CreateFence",
    "CreateCommandAllocator","CreateSwapChainForHwnd","GetBuffer","ResizeBuffers1",
})


# ID3D12DescriptorHeap* ppDescHeaps_204[0x2] = (pDescHeap_1, pDescHeap_4);
# pCmdList_21->SetDescriptorHeaps(NumDescriptorHeaps = 0x2, ppDescriptorHeaps = ppDescHeaps_204);

pCmdList = set({"SetGraphicsRootConstantBufferView","IASetIndexBuffer","SetPipelineState","IASetPrimitiveTopology",
                "ClearRenderTargetView","Close","OMSetRenderTargets","Reset",
                "SetGraphicsRootDescriptorTable","RSSetViewports","SetDescriptorHeaps","DrawIndexedInstanced",
                "RSSetScissorRects","IASetVertexBuffers","ClearDepthStencilView","SetGraphicsRootSignature",
                "ResourceBarrier","SetComputeRootDescriptorTable","SetComputeRootConstantBufferView","SetComputeRootSignature",
                "ClearUnorderedAccessViewUint","CopyBufferRegion","DiscardResource","SetComputeRoot32BitConstants",
                "SetGraphicsRoot32BitConstants","DrawInstanced","Dispatch","CopyTextureRegion",
                "ClearUnorderedAccessViewFloat","CopyResource","ExecuteIndirect",
                })

pCmdList_set_func = set({"SetDescriptorHeaps","Close"})

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














