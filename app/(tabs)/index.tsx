import { View, Text, TouchableOpacity } from 'react-native';
import { useState } from 'react';

export default function TabOneScreen() {
  const [count, setCount] = useState(0);

  return (
    <View className="flex-1 items-center justify-center bg-blue-500">
      <View className="bg-white p-8 rounded-2xl shadow-lg">
        <Text className="text-4xl font-bold text-blue-600 mb-4 text-center">
          Tailwind Test ✅
        </Text>
        
        <Text className="text-xl text-gray-700 mb-6 text-center">
          Count: {count}
        </Text>
        
        <TouchableOpacity 
          onPress={() => setCount(count + 1)}
          className="bg-blue-500 px-6 py-4 rounded-lg active:bg-blue-600">
          <Text className="text-white font-semibold text-center text-lg">
            Click Me!
          </Text>
        </TouchableOpacity>
        
        <TouchableOpacity 
          onPress={() => setCount(0)}
          className="bg-red-500 px-6 py-4 rounded-lg mt-3 active:bg-red-600">
          <Text className="text-white font-semibold text-center text-lg">
            Reset
          </Text>
        </TouchableOpacity>
      </View>
      
      <View className="mt-8">
        <Text className="text-white text-lg font-bold mb-2">
          🎨 Colors Working
        </Text>
        <Text className="text-yellow-300 text-lg font-bold mb-2">
          📏 Spacing Working
        </Text>
        <Text className="text-green-300 text-lg font-bold">
          ✨ Styles Working
        </Text>
      </View>
    </View>
  );
}