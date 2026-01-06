import triton_python_backend_utils as pb_utils
import json

class TritonPythonModel:
    def initialize(self, args):
        print("模型初始化...")
        
    def execute(self, requests):
        responses = []
        for request in requests:
            # 获取输入
            in_tensor = pb_utils.get_input_tensor_by_name(request, "input")
            input_text = in_tensor.as_numpy()[0]
            
            # 简单的处理逻辑（示例）
            result = f"处理结果: {input_text}"
            
            # 创建输出
            out_tensor = pb_utils.Tensor("output", [result.encode()])
            response = pb_utils.InferenceResponse(output_tensors=[out_tensor])
            responses.append(response)
            
        return responses
        
    def finalize(self, args):
        print("模型清理...")
