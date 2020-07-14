// Fill out your copyright notice in the Description page of Project Settings.


#include "CustomPathfindingLibrary.h"
#include <queue>
#include <stdlib.h> 

class MapLoc {
public:
	MapLoc(int x, int y, float cost);
	int getX() const;
	int getY() const;
	float getCost() const;
	friend bool operator < (const MapLoc& lhs, const MapLoc& rhs);
	friend bool operator > (const MapLoc& lhs, const MapLoc& rhs);

private:
	int x;
	int y;
	float cost;
};


int c = 10;
const int h = 5;
const int w = 5;
int tempMap[] = {0,0,0,0,0,
				 0,1,1,1,0,
				 0,1,0,1,0,
				 0,1,0,1,0,
				 0,0,0,0,0};

int xOffset[] = {0,0,1,-1};
int yOffset[] = {1,-1,0,0};

int sx = 1;
int sy = 3;
FVector2D start = FVector2D(sx, sy);

FString UCustomPathfindingLibrary::TestFunc(int a, int b)
{
	int foo = a + b + c;
	FVector2D t1 = FVector2D(1.0,1.0);
	FVector2D t2 = FVector2D(2.0, 3.0);
	FVector2D t3 = t1 + t2;
	return FString::Printf(TEXT("Hello world %f %f"), t3.X, t3.Y);
}

TArray<FVector2D> UCustomPathfindingLibrary::getPath(int gx, int gy)
{
	int xPointer[h*w];
	int yPointer[h*w];
	bool checkedMap[h*w];
	std::priority_queue<MapLoc, std::vector<MapLoc>, std::greater<MapLoc> > q;
	MapLoc startLoc = MapLoc(sx, sy, (abs(sx - gx) + abs(sy - gy)));
	q.push(startLoc);

	for (int i = 0; i < h*w; i++) {
		checkedMap[i] = false;
		xPointer[i] = 0;
		yPointer[i] = 0;
	}

	bool found = false;
	while (!q.empty()){
		MapLoc current = q.top();
		if (current.getX() == gx && current.getY() == gy) {
			found = true;
			break;
		}
		checkedMap[current.getY() * w + current.getX()] = true;
		q.pop();

		for (int i = 0; i < 4; i++) {
			int nx = current.getX() + xOffset[i];
			int ny = current.getY() + yOffset[i];
			int index = ny * w + nx;
			if (checkedMap[index] || tempMap[index] == 0) {
				continue;
			}
			float nG = current.getCost() + 1.0;
			float nH = abs(current.getX() - gx) + abs(current.getY() - gy);
			float nF = nG + nH;
			xPointer[index] = current.getX();
			yPointer[index] = current.getY();
			q.push(MapLoc(nx, ny, nF));
		}
		
	}

	TArray<FVector2D> ans;
	if (found) {
		int indexGoal = gy * w + gx;
		int indexStart = sy * w + sx;
		ans.Add(FVector2D(gx,gy));
		while (indexGoal != indexStart) {
			int cx = xPointer[indexGoal];
			int cy = yPointer[indexGoal];
			ans.Add(FVector2D(cx, cy));
			indexGoal = cy * w + cx;
		}
	}
	return ans;
}


// MapLoc Functions...

MapLoc::MapLoc(int x, int y, float cost): x(x), y(y), cost(cost)
{
}

float MapLoc::getCost() const
{
	return cost;
}

int MapLoc::getX() const
{
	return x;
}

int MapLoc::getY() const
{
	return y;
}


bool operator<(const MapLoc & lhs, const MapLoc & rhs)
{
	return lhs.getCost() < rhs.getCost();
}
bool operator>(const MapLoc & lhs,const MapLoc & rhs)
{
	return lhs.getCost() > rhs.getCost();
}