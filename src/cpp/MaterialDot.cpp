//
// Created by aleksei on 24.02.18.
//

#include "MaterialDot.hpp"

MaterialDot::MaterialDot(double x, double y, double z, double _m) {
    coordinates = {x, y, z};
    velocity = {0, 0, 0};
    m = _m;
}

MaterialDot::MaterialDot(const double *coords, double _m) {
    coordinates = {coords[0], coords[1], coords[2]};
    velocity = {0, 0, 0};
    m = _m;
}

Vector MaterialDot::getCoordinates() const noexcept {
    return coordinates;
}

Vector MaterialDot::getVelocity() const noexcept {
    return velocity;
}

void MaterialDot::setVelocity(const Vector &v) noexcept {
    velocity = v;
}

double MaterialDot::getMass() const noexcept {
    return m;
}

void MaterialDot::evolute(const Vector& force, const double t) {
    coordinates = coordinates + 0.5/m*t*t*force + velocity*t;
    velocity = velocity + t/m*force;
}

bool MaterialDot::operator==(const MaterialDot &other) const {
    return (m == other.getMass()
            && velocity == other.getVelocity()
            && coordinates == other.getCoordinates());
}

bool MaterialDot::operator!=(const MaterialDot &other) const {
    return !(*this == other);
}


// Redefinition of hash function
namespace std {

        std::size_t hash<MaterialDot>::operator() (const MaterialDot& dot) const
        {
            using std::size_t;
            using std::hash;

            // Compute individual hash values for first,
            // second and third and combine them using XOR
            // and bit shifting:

            return ((hash<double>()(dot.getCoordinates().toArray().back())
                     ^ (hash<double>()(dot.getVelocity().toArray().back()) << 1)) >> 1)
                   ^ (hash<double>()(dot.getMass()) << 1);
        }

        std::size_t hash<std::pair<MaterialDot, MaterialDot>>::operator()(
            const std::pair<MaterialDot, MaterialDot> &pair) const {
            return std::hash<MaterialDot>()(pair.first) ^ std::hash<MaterialDot>()(pair.second);
        }
}