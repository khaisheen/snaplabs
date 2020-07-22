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
		static TArray<FVector> getPath(int sx, int sy, int gx, int gy, int z);

	UFUNCTION(BlueprintCallable, Category = "MyCustomLibrary")
		static TArray<FVector> getFullPath(int sx, int sy, int sz, int gx, int gy, int gz);
		
};
