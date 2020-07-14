// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "CustomPathfindingLibrary.generated.h"

/**
 * 
 */
UCLASS()
class CIRCLESMALONE_API UCustomPathfindingLibrary : public UBlueprintFunctionLibrary
{
	GENERATED_BODY()
		UFUNCTION(BlueprintCallable, Category = "MyCustomLibrary")
		static FString TestFunc(int a, int b);

		UFUNCTION(BlueprintCallable, Category = "MyCustomLibrary")
		static TArray<FVector2D> getPath(int gx, int gy);
		
};
